from __future__ import annotations
import logging
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User

from ...celery import TaskInfo, CeleryMonitor

_channel_layer = get_channel_layer()
_group_add = async_to_sync(_channel_layer.group_add)
_group_discard = async_to_sync(_channel_layer.group_discard)

class TaskListWebsocket(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.logger = logging.getLogger(__name__+'.'+type(self).__qualname__)
        self.monitor = CeleryMonitor.get_instance()
    

    def connect(self):
        self.user: User = self.scope['user']
        if not self.user.is_superuser:
            self.logger.debug("reject user %s, channel: %s", self.user, self.channel_name)
            self.accept()
            self.close(3000) # unauthorized
            return
        
        self.logger.debug("connect user %s, channel: %s", self.user, self.channel_name)
        _group_add(TaskInfo.get_channel_group_name('*'), self.channel_name)
        self.accept()

        previous_tasks = self.monitor.previous_or_start()
        if previous_tasks:
            self.send_json({"tasks": [task.as_dict() for task in previous_tasks.values()]})

        if self.monitor.not_working:
            self.close(4181) # celery_not_working


    def disconnect(self, code):
        self.logger.debug("disconnect user %s, code: %s, channel: %s", self.user, code, self.channel_name)
        _group_discard(TaskInfo.get_channel_group_name('*'), self.channel_name)


    @classmethod
    def encode_json(cls, content):
        return json.dumps(content, ensure_ascii=False, cls=DjangoJSONEncoder)


    def send_serialized(self, data):
        """
        Callback for `group_send()` used in `TaskInfo.send()`.
        """
        serialized = data['serialized']
        self.send(serialized)


class TaskDetailWebsocket(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.logger = logging.getLogger(__name__+'.'+type(self).__qualname__)
        self.monitor = CeleryMonitor.get_instance()

    def connect(self):
        self.task_id = str(self.scope['url_route']['kwargs']['id'])
        self.user: User = self.scope['user']
        if not self.user.is_authenticated:
            self.logger.debug("reject user %s, channel: %s", self.user, self.channel_name)
            self.accept()
            self.close(3000) # unauthorized
            return
        
        self.logger.debug("connect user %s, channel: %s", self.user, self.channel_name)
        _group_add(TaskInfo.get_channel_group_name(self.task_id), self.channel_name)
        self.accept()

        previous_tasks = self.monitor.previous_or_start()
        if previous_tasks and self.task_id in previous_tasks:
            self.send_json({"task": previous_tasks[self.task_id].as_dict()})

        if self.monitor.not_working:
            self.close(4181) # celery_not_working


    def disconnect(self, code):
        self.logger.debug("disconnect user %s, code: %s, channel: %s", self.user, code, self.channel_name)
        _group_discard(TaskInfo.get_channel_group_name(self.task_id), self.channel_name)


    @classmethod
    def encode_json(cls, content):
        return json.dumps(content, ensure_ascii=False, cls=DjangoJSONEncoder)


    def send_serialized(self, data):
        """
        Callback for `group_send()` used in `TaskInfo.send()`.
        """
        serialized = data['serialized']
        self.send(serialized)
