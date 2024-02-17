import logging
from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from ....celery import get_task_by_name, convert_task_string_args

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser):
        parser.add_argument('name_and_args', nargs='+', help="Name (and optional args) of the task to execute.")
        parser.add_argument('-d', '--delay', type=float, help="Delay in seconds.")
        parser.add_argument('-s', '--sync', action='store_true', help="Run the task synchronously.")
    
    def handle(self, name_and_args: list[str], delay: float = None, sync: bool = False, **options):
        name = name_and_args[0]
        args = name_and_args[1:]

        task = get_task_by_name(name)
        args, kwargs = convert_task_string_args(task, *args)

        msg = f"run task {task.name}"
        if sync:
            msg += f" synchronously"
        elif delay is not None:
            msg += f" with {delay} second delay"
        if args:
            msg += f", args={args}"
        if kwargs:
            msg += f", kwargs={kwargs}"
        logger.info(msg)

        if sync:
            task(*args, **kwargs)
        else:
            result = task.apply_async(args, kwargs, countdown=delay)
            logger.info(f"task id: {result.id}")
            result.forget()
