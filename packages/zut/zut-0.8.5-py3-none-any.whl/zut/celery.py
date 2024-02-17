"""
Utilities for Celery infrastructure:

- Add `ISSUE` custom state: task executed successfully but some warnings or errors were logged . Activate it using `configure_issue_detection` in your main `celery` module.
- Add `PROGRESS` custom state.
- Monitoring.
"""
from __future__ import annotations
from importlib import import_module
import inspect

import json
import logging
import re
from configparser import _UNSET
from datetime import datetime
from enum import Enum
from threading import Thread, Timer
from time import time_ns
from uuid import UUID

from asgiref.sync import async_to_sync
from celery import Task, states, current_app, current_task
from celery.result import AsyncResult
from celery.signals import after_setup_task_logger, task_postrun
from celery.utils.log import get_task_logger
from django.conf import settings

from .json import ExtendedJSONEncoder
from .types import convert

try:
    # prefer django version as local timezone might be configured globally to something different as system timezone
    from django.utils.timezone import is_aware, make_aware
except:
    from .date import is_aware, make_aware

logger = get_task_logger(__name__)

_issue_handler = None

class CeleryState(Enum):
    """
    Celery predefined and custom states, by order of precedence.
    """
    SUCCESS = states.SUCCESS
    """ Task has been successfully executed. """
    
    FAILURE = states.FAILURE
    """ Task execution resulted in failure. """
    
    ISSUE = 'ISSUE'
    """ Task executed successfully but some warnings or errors were logged (custom state)."""
    
    PROGRESS = 'PROGRESS'
    """ Task sent a progress report (custom state)."""
    
    REVOKED = states.REVOKED
    """ Task has been revoked. """
    
    STARTED = states.STARTED
    """ Task has been started. """
    
    RECEIVED = states.RECEIVED
    """ Task was received by a worker (only used in events). """
    
    SCHEDULED = 'SCHEDULED'
    """ Task was received by a worker with an ETA (custom state, only used in TaskMonitoringInfo). """
    
    REJECTED = states.REJECTED
    
    RETRY = states.RETRY
    """ Task will be retried. """

    PENDING = states.PENDING
    """ Task is waiting for execution or unknown. """

    
def configure_issue_detection():
    global _issue_handler  # make it global to avoid garbage-collection

    _issue_handler = CeleryIssueHandler()
    _issue_handler.connect()


class CeleryIssueHandler(logging.Handler):
    def __init__(self, level=logging.WARNING):
        self.task_counts: dict[str,dict[int, int]] = {}
        super().__init__(level=level)

    def emit(self, record: logging.LogRecord):
        if record.levelno < self.level:
            return
        
        task_id = getattr(record, 'task_id', None)
        if not task_id:
            return
        
        if not task_id in self.task_counts:
            counts = {}
            self.task_counts[task_id] = counts
        else:
            counts = self.task_counts[task_id]

        if not record.levelno in counts:
            counts[record.levelno] = 1
        else:
            counts[record.levelno] += 1

    def get_task_issue(self, task_id: str):
        counts = self.task_counts.get(task_id)
        if not counts:
            return {}
        
        result = {}
        for levelno, count in counts.items():
            level = logging.getLevelName(levelno)
            if isinstance(level, str):
                level = level.lower()
            result[level] = count
        return result
    
    def clear_task_issue(self, task_id: str):
        counts = self.task_counts.get(task_id)
        if counts:
            counts.clear()
    
    def connect(self):        
        after_setup_task_logger.connect(self.on_after_setup_task_logger)
        task_postrun.connect(self.on_task_postrun)

    def on_after_setup_task_logger(self, logger: logging.Logger, **kwargs):
        logger.addHandler(self)

    def on_task_postrun(self, task_id: str, task: Task, **kwargs):
        issue = self.get_task_issue(task_id)
        if not issue:
            return
        
        r: AsyncResult = task.AsyncResult(task_id)
        if r.state != CeleryState.SUCCESS.value:
            self.clear_task_issue(task_id) # do not keep counts of previous retries
            return
        
        meta = {"result": r.info, "issue": issue}
        task.update_state(task_id, CeleryState.ISSUE.value, meta=meta)
        task.send_event(f'task-{CeleryState.ISSUE.value.lower()}', **meta)


def is_celery_working():
    logger = logging.getLogger(__name__)

    try:
        current_app.broker_connection().ensure_connection(max_retries=1)
    except Exception as err:
        logger.exception(f"cannot connect to celery broker: {err}")
        return False

    result: list[dict] = current_app.control.ping()
    if not result:
        logger.error(f"no celery worker found")
        return False
    
    return True


_progress_logger = get_task_logger(f"{__name__}:progress")


class Progress:
    def __init__(self, index: int|float, total: int|float, step: int|float = None):
        self.index = index
        
        if isinstance(total, (int,float)):
            self.total = total
        else:
            self.total = len(total)

        if step is not None:
            self.step = step
        elif (isinstance(self.index, int) or (isinstance(self.index, float) and self.index.is_integer())) and (isinstance(self.total, int) or (isinstance(self.total, float) and self.total.is_integer())):
            self.step = 1
        else:
            raise ValueError(f"step required for non-int index/total: {self.index}/{self.total}")

    def sub(self, index: int, size: int):
        if not isinstance(size, int):
            size = len(size)
        
        sub_step = self.step / size
        sub_index = self.index + index * sub_step

        return Progress(sub_index, self.total, sub_step)


_progress_update_state = None

def report_progress(message: str = None, progress: Progress = None, *, index: int|float = None, total: int|float = None, details: str = None):
    """
    - `message`: public information, will be send to client.
    - `details`: private details, only displayed in logs and result backend. Not sent to client.
    """
    global _progress_update_state

    if not message and not progress and not details and index is None and total is None:
        logger.error(f"cannot report progress with only empty arguments")
        return
    
    if progress:
        if index is not None or total is not None:
            logger.error(f"cannot report progress with `progress` argument given along with `index` or `total` arguments")
            return
        index = progress.index
        total = progress.total
    
    meta = {}
    log_message = None

    if index is not None:
        meta["index"] = index

        log_message = f"["

        if total is not None:
            meta["total"] = total
            if total != 0:
                log_message += f"{100*index/total:.0f}%, "

        log_message += f'{index:,.2f}' if isinstance(index, float) and not index.is_integer() else f'{index:,}'
        if total is not None:
            log_message += f"/{f'{total:,.2f}' if isinstance(total, float) and not total.is_integer() else f'{total:,}'}"

        log_message += f"]"
    else:    
        if total is not None:
            logger.error(f"cannot report progress with a `total` argument but no `index` argument")
            return

    if message:
        message = message[0].upper() + message[1:]
        meta["message"] = message
        log_message = (f"{log_message} " if log_message else "") + message

    if details:
        meta["details"] = details
        log_message = (f"{log_message} - " if log_message else "") + f"Details: {details}"

    _progress_logger.info(log_message)

    if not current_task:
        return # not executed using celery
    if not current_task.request.id:
        return # executed synchronously

    current_task.send_event(f'task-{CeleryState.PROGRESS.value.lower()}', **meta)
    
    if _progress_update_state is None:
        # By default, do not update the state for progress message,
        # i.e. do not update the database (to avoid solliciting it too much)
        # Task can still be monitored using events
        _progress_update_state = getattr(settings, 'CELERY_PROGRESS_UPDATE_STATE', False)
            
    if _progress_update_state:
        print("HERE")
        current_task.update_state(state=CeleryState.PROGRESS.value, meta=meta)


class CeleryMonitor:    
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is not None:
            return cls._instance
        
        cls._instance = CeleryMonitor()
        return cls._instance

    def __init__(self):
        if type(self)._instance:
            raise ValueError(f"An instance of {type(self).__name__} has already been created.")
        else:
            type(self)._instance = self

        self._logger = logging.getLogger(f'{__name__}.{type(self).__qualname__}')
        self._taskinfo_dict: dict[str,TaskInfo] = {}
        self._started = False

        self.not_working = False

        try:
            from django_celery_results.models import TaskResult
            self.TaskResult = TaskResult
        except:
            self.TaskResult = None


    def get(self, task_id: str, fallback = _UNSET):
        if isinstance(task_id, UUID):
            task_id = str(task_id)

        if fallback is _UNSET:
            return self._taskinfo_dict[task_id]
        else:
            return self._taskinfo_dict.get(task_id)


    def forget(self, *task_ids: str):        
        if self.TaskResult:
            self.TaskResult.objects.filter(task_id__in=[str(task_id) if isinstance(task_id, UUID) else task_id for task_id in task_ids]).delete()
        
        for task_id in task_ids:
            if isinstance(task_id, UUID):
                task_id = str(task_id)

            if task_id in self._taskinfo_dict:
                del self._taskinfo_dict[task_id]


    def previous_or_start(self):
        """
        Main entry point:
        - If monitoring was already started, return previously found tasks.
        - Otherwise, start monitoring and return an empty list: tasks will be sent when they are discovered.
        """
        if self._started:
            return self._taskinfo_dict
        
        else:
            self.start()
            return None
        

    def start(self):
        self._started = True
        self._logger.info("start tasks monitoring")

        if self.TaskResult:
            self._retrieve_from_results()

        threads: list[Thread] = []        

        if not is_celery_working():
            self.not_working = True
            return threads
        
        threads.append(self._retrieve_from_events())
        threads.append(self._retrieve_from_workers())
        return threads


    def _retrieve_from_results(self):
        """
        Retrieve tasks from results backend (database).

        All tasks except those not yet started (e.g. received with an ETA) should be available.
        """
        for tr in self.TaskResult.objects.all():        
            self._logger.debug("from results backend: %s", tr.__dict__)

            info, _ = self._get_or_create_taskinfo(tr.task_id)
            info.name = tr.task_name
            info.params = self._get_params_from_args_and_kwargs(tr.task_args, tr.task_kwargs)
            info.worker = tr.worker
            info.state = tr.status
            
            result = json.loads(tr.result)

            # Percent
            if info.state in [CeleryState.SUCCESS.value, CeleryState.ISSUE.value]:
                info.progress = 100.0
            elif info.state == CeleryState.PROGRESS.value:
                index = result.pop('index', None)
                total = result.pop('total', None)
                info.progress = self._get_percent_from_progress(info.progress, index, total)
            elif info.state == CeleryState.STARTED.value:
                info.progress = 0.0
            else:
                info.progress = None
            
            # Details
            if info.state in [CeleryState.FAILURE.value, CeleryState.REVOKED.value, CeleryState.RETRY.value]:
                exc_type = result['exc_type']
                exc_details = ' - '.join(str(value) for value in result['exc_message']) if isinstance(result['exc_message'], list) else result['exc_message']
                if info.state == CeleryState.REVOKED.value and exc_type == 'TaskRevokedError' and exc_details in ['terminated', 'revoked']:
                    info.details = exc_details.capitalize()
                else:
                    info.details = f"{exc_type}: {exc_details}"
            elif result is not None:
                if info.state in CeleryState.ISSUE.value:
                    info.details = self._get_details_from_result(result.get('result'), result.get('issue'))
                elif info.state in CeleryState.SUCCESS.value:
                    info.details = f"Result: {result}"
                else:
                    info.details = f"{result}"
            else:
                info.details = None

            # Start and end
            info.start = tr.date_created.astimezone()
            if not info.state in [CeleryState.STARTED.value, CeleryState.PROGRESS.value]:
                info.end = tr.date_done.astimezone()

            info.handle()


    def _retrieve_from_events(self):
        """
        Retrieve/update tasks from live notifications.
        """
        thread = Thread(target=self._capture_events, name='capture-events')
        thread.daemon = True
        thread.start()
        return thread


    def _capture_events(self):
        with current_app.connection() as connection:
            receiver = current_app.events.Receiver(connection, handlers={'*': self._on_event})
            receiver.capture(limit=None, timeout=None, wakeup=True)


    def _on_event(self, event: dict):
        event_type: str = event['type']
        if not event_type.startswith('task-'):
            return
        
        self._logger.debug("event %s: %s", event_type, event)

        info, _ = self._get_or_create_taskinfo(event['uuid'])
        info.worker = event['hostname']
        
        if event_type == 'task-received':
            info.name = event['name']
            info.params = self._get_params_from_args_and_kwargs(event['args'], event['kwargs'])
            if event['eta']:
                info.state = CeleryState.SCHEDULED.value
                info.start = self._get_datetime_from_isoformat(event['eta'])
            else:
                info.state = CeleryState.RECEIVED.value
            info.progress = None
        
        elif event_type == 'task-started':
            info.state = CeleryState.STARTED.value
            info.start = self._get_datetime_from_timestamp(event['timestamp'])
            info.details = None
            info.progress = 100.0

        elif event_type == 'task-progress':
            info.state = CeleryState.PROGRESS.value
            info.details = event['message']

            index = event.get('index')
            total = event.get('total')
            info.progress = self._get_percent_from_progress(info.progress, index, total)

        elif event_type == 'task-retried':
            info.state = CeleryState.RETRY.value
            info.details = self._get_details_from_event_exception(event['exception'])
            info.end = self._get_datetime_from_timestamp(event['timestamp'])
            info.progress = None

        elif event_type == 'task-succeeded':
            if info.state != CeleryState.ISSUE.value: # NOTE: 'task-issue' event is received before the 'task-succeeded' that actually triggered id
                info.state = CeleryState.SUCCESS.value
                info.details = self._get_details_from_result(event['result'])
                info.end = self._get_datetime_from_timestamp(event['timestamp'])
                info.progress = 100.0

        elif event_type == 'task-issue':
            info.state = CeleryState.ISSUE.value
            info.details = self._get_details_from_result(event['result'], event['issue'])
            info.end = self._get_datetime_from_timestamp(event['timestamp'])
            info.progress = 100.0

        elif event_type == 'task-failed':
            info.state = CeleryState.FAILURE.value
            info.details = self._get_details_from_event_exception(event['exception'])
            info.end = self._get_datetime_from_timestamp(event['timestamp'])
            info.progress = None

        elif event_type == 'task-revoked':
            info.state = CeleryState.REVOKED.value
            info.details = 'Terminated' if event['terminated'] else 'Revoked'
            info.end = self._get_datetime_from_timestamp(event['timestamp'])
            info.progress = None

        else:
            info.state = event_type[len('task-'):].upper()
            info.details = None
            info.progress = None

        info.handle()


    def _retrieve_from_workers(self):
        thread = Thread(target=self._inspect_workers, name='inspect-workers')
        thread.daemon = True
        thread.start()
        return thread


    def _inspect_workers(self):
        """
        Retrieve received but not yet started tasks from workers inspection.

        Other tasks should be available through results backend (database).
        """
        inspected = current_app.control.inspect()

        # revoked
        if result_dict := inspected.revoked():
            worker_revoked: dict[str,set[str]] = {worker: set(task_ids) for worker, task_ids in result_dict.items()}
        else:
            worker_revoked = {}
        
        # reserved: have been received, but are still waiting to be executed
        if result_dict := inspected.reserved():
            for worker, worker_data in result_dict.items():
                for task_info in worker_data:
                    self._update_from_worker(worker, 'reserved', task_info, revoked_task_ids=worker_revoked.get(worker))
                    
        # scheduled: have been received, but are still waiting to be executed (these are tasks with an ETA/countdown argument, not periodic tasks).
        if result_dict := inspected.scheduled():
            for worker, worker_data in result_dict.items():
                for schedule_info in worker_data:
                    task_info = schedule_info['request']
                    eta = schedule_info['eta']
                    self._update_from_worker(worker, 'scheduled', task_info, eta=eta, revoked_task_ids=worker_revoked.get(worker))

        if not self.TaskResult:
            if result_dict := inspected.active():
                for worker, worker_data in result_dict.items():
                    for task_info in worker_data:
                        self._update_from_worker(worker, 'active', task_info, revoked_task_ids=worker_revoked.get(worker))

                

    def _update_from_worker(self, worker: str, funcname: str, task_info: dict, *, revoked_task_ids: set[str], eta: str = None):
        task_id = task_info['id']
        is_revoked = task_id in revoked_task_ids

        self._logger.debug("from worker %s (%s): %s, eta=%s, is_revoked=%s", funcname, worker, task_info, eta, is_revoked)

        info, need_send = self._get_or_create_taskinfo(task_id)

        if info.worker is None:
            info.worker = worker
            need_send = True

        if info.state is None:
            if is_revoked:
                info.state = CeleryState.REVOKED.value
            else:
                info.state = CeleryState.STARTED.value if funcname == 'active' else funcname.upper()
            need_send = True

        if info.name is None:
            info.name = task_info['name']
            need_send = True

        if info.params is None:
            info.params = self._get_params_from_args_and_kwargs(task_info['args'], task_info['kwargs'])
            if info.params is not None:
                need_send = True

        if info.start is None:
            if funcname == 'scheduled' and eta:
                info.start = self._get_datetime_from_isoformat(eta)
                need_send = True
            elif funcname == 'active' and task_info['time_start']:
                info.start = self._get_datetime_from_timestamp(task_info['time_start'])
                need_send = True

        if need_send:        
            info.handle()
        

    def _get_params_from_args_and_kwargs(self, args: str, kwargs: str):
        if not isinstance(args, str):
            args = str(args)
        if (args.startswith('(') and args.endswith(')')) or (args.startswith('[') and args.endswith(']')):
            args = args[1:-1]
        elif (args.startswith('"(') and args.endswith(')"')) or (args.startswith('"[') and args.endswith(']"')):
            args = args[2:-2]
        args = args.strip()
        if args.endswith(','):
            args = args[:-1]

        if not isinstance(kwargs, str):
            kwargs = str(kwargs)
        if kwargs.startswith('{') and kwargs.endswith('}'):
            kwargs = kwargs[1:-1]
        elif kwargs.startswith('"{') and kwargs.endswith('}"'):
            kwargs = kwargs[2:-2]
        kwargs = kwargs.strip()

        params = None
        if args:
            params = (f"{params}, " if params else "") + args
        if kwargs:
            params = (f"{params}, " if params else "") + kwargs
        return params
    
    
    def _get_details_from_event_exception(self, exc_report: str):
        if m := re.match(r'^([a-zA-Z0-9_]+)\(["\'](.+)["\']\)$', exc_report):
            return f"{m[1]}: {m[2]}"
        else:
            return exc_report
        

    def _get_details_from_result(self, result: str, issue: dict = None):
        details = None

        if result and result != 'None':
            if isinstance(result, str) and result.startswith("'") and result.endswith("'"):
                result = result[1:-1]
            details = f"Result: {result}"

        if issue:
            for level, count in issue.items():
                details = (f'{details} - ' if details else '') + f"{level.capitalize()}: {count}"
        
        return details


    def _get_datetime_from_isoformat(self, isoformat: str):
        dt = datetime.fromisoformat(isoformat)
        if not is_aware(dt):
            dt =  make_aware(dt)
        return dt
    

    def _get_datetime_from_timestamp(self, timestamp: float):
        return make_aware(datetime.fromtimestamp(timestamp))
    
    
    def _get_percent_from_progress(self, percent, index, total):
        if index is not None and total is not None and total > 0:
            return 100 * index / total
        else:
            return percent


    def _get_or_create_taskinfo(self, id: str):
        if isinstance(id, UUID):
            id = str(id)
        
        if id in self._taskinfo_dict:
            created = False
            return self._taskinfo_dict[id], created
        else:
            created = True
            info = TaskInfo(id)
            self._taskinfo_dict[id] = info
            return info, created


def _current_seconds():
    return time_ns() / 1e9

_group_send = None
_progress_minimal_interval = None

class TaskInfo:
    def __init__(self, id: str):
        global _group_send, _progress_minimal_interval

        self.id = id
        self.name: str|None = None
        self.params: str|None = None
        self.worker: str|None = None
        self.state: str|None = None
        self.progress: float|None = None
        self.details: str|None = None
        self.start: datetime|None = None
        self.end: datetime|None = None

        self._handle_num = 0
        self._last_sent: int|None = None
        self._delayed_timer: Timer|None = None

        if _group_send is None:
            try:
                from channels.layers import get_channel_layer
                channel_layer = get_channel_layer()
                _group_send = async_to_sync(channel_layer.group_send)
            except ImportError:
                _group_send = False
            
            _progress_minimal_interval = getattr(settings, 'CELERY_PROGRESS_MINIMAL_INTERVAL', 0.5)


    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "params": self.params,
            "worker": self.worker,
            "state": self.state,
            "progress": self.progress,
            "details": self.details,
            "start": self.start,
            "end": self.end,
        }

    def handle(self):
        if not _group_send:
            return
        
        self._handle_num += 1
        
        if self._delayed_timer:
            self._delayed_timer.cancel()
            self._delayed_timer = None
        
        t = _current_seconds()
        
        if _progress_minimal_interval and self.state == CeleryState.PROGRESS.value:
            if self._last_sent is not None and t - self._last_sent < _progress_minimal_interval:
                # Do not send progress messages more than the defined interval.
                # Instead, delay the message for the remaining time, and send it only if no new message appeared
                self._delayed_timer = Timer(_progress_minimal_interval - (t - self._last_sent), self._timer_callback, [self._handle_num])
                self._delayed_timer.start()
                return
        
        self._actual_send()
        self._last_sent = t

    def _timer_callback(self, handle_num):
        if self._handle_num != handle_num:
            # Another message has appeared
            return
        
        self._actual_send()
        self._last_sent = _current_seconds()

    def _actual_send(self):
        message = {
            "type": "send_serialized",
            "serialized": json.dumps({"task": self.as_dict()}, ensure_ascii=False, cls=ExtendedJSONEncoder),
        }
        _group_send(self.get_channel_group_name('*'), message)
        _group_send(self.get_channel_group_name(self.id), message)
    
    @classmethod
    def get_channel_group_name(cls, task_id):
        if task_id == '*':
            return f"tasks"
        else:
            return f"task-{task_id}"


def get_task_by_name(name: str):
    _ensure_tasks_module_loaded()

    all_tasks = get_all_tasks_by_name()
    if name in all_tasks:
        return all_tasks[name]
    
    task_names = [task_name for task_name in all_tasks.keys() if task_name.endswith(f'.{name}')]
    if len(task_names) == 1:
        return all_tasks[task_names[0]]
    
    if len(task_names) > 1:
        raise ValueError(f"Several task match name \"{name}\": {', '.join(task_names)}.")
    
    raise ValueError(f"No task match name \"{name}\".")


def get_all_tasks_by_name() -> dict[str,Task]:
    _ensure_tasks_module_loaded()
    return current_app.tasks


_ensured_tasks_module_loaded = False

def _ensure_tasks_module_loaded():
    from django.apps import apps

    global _ensured_tasks_module_loaded
    if _ensured_tasks_module_loaded:
        return
    
    for app in apps.get_app_configs():
        task_module_name = f'{app.module.__name__}.tasks'
        try:
            import_module(task_module_name)
        except ImportError:
            pass

    _ensured_tasks_module_loaded = True


def convert_task_string_args(task, *args):
    if not args:
        return tuple(), dict()
    
    # Determine argument types
    signature = inspect.signature(task.run)
    var_positional_type = None
    var_keyword_type = None
    parameter_types = {}
    positional_types = []
    for parameter in signature.parameters.values():
        parameter_type = None if parameter.annotation is inspect.Parameter.empty else parameter.annotation
        if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            var_positional_type = parameter_type
        elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
            var_keyword_type = parameter_type
        else:
            parameter_types[parameter.name] = parameter_type
            if parameter.kind in [inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD]:
                positional_types.append(parameter_type)
    
    # Distinguish args and kwargs
    positionnal_args = []
    keyword_args = {}
    for arg in args:
        if m := re.match(r'^([a-z0-9_]+)=(.+)$', arg):
            keyword_args[m[1]] = m[2]
        else:
            positionnal_args.append(arg)

    # Convert kwargs
    for parameter, value in keyword_args.items():
        if parameter in parameter_types:
            target_type = parameter_types[parameter]
            if target_type:
                keyword_args[parameter] = convert(value, target_type)

        elif var_keyword_type:
            keyword_args[parameter] = convert(value, var_keyword_type)

    # Convert args
    for i, value in enumerate(positionnal_args):
        if i < len(positional_types):
            target_type = positional_types[i]
            if target_type:
                positionnal_args[i] = convert(value, target_type)

        elif var_positional_type:
            positionnal_args[i] = convert(value, var_positional_type)

    return positionnal_args, keyword_args
