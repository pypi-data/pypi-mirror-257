import shlex
from celery import current_app
from celery.utils.log import get_task_logger
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import DetailView, TemplateView, View
from zut.django.mixins import IsAuthenticatedMixin, IsSuperuserMixin
from ...celery import CeleryMonitor, TaskInfo, is_celery_working, get_all_tasks_by_name, get_task_by_name, convert_task_string_args

logger = get_task_logger(__name__)

class TaskListView(IsSuperuserMixin, TemplateView):
    template_name = 'zut/celery_task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        def sortkey(task_name: str):
            if task_name.startswith('celery.'):
                return (999, task_name)
            elif task_name == 'zut.django.tasks.demo':
                return (0, task_name)
            else:
                return (1, task_name)

        context['task_list'] = [{'name': task_name, 'display_name': task_name} for task_name in sorted(get_all_tasks_by_name().keys(), key=lambda task_name: sortkey(task_name))]
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        if not is_celery_working():
            return HttpResponseServerError(_("Celery is not working."))
        
        action = request.POST.get('action')
        if not action:
            return HttpResponseBadRequest(_("Missing: %s.") % "action")
        
        task_ids = request.POST.get('task_ids', '').split(';')
        if not task_ids or '' in task_ids:
            return HttpResponseBadRequest(_("Missing: %s.") % "task_ids")
    
        if action == 'terminate':
            for task_id in task_ids:
                current_app.control.revoke(task_id, terminate=True)
            return HttpResponse(_("Termination request sent."))
    
        elif action == 'revoke':
            for task_id in task_ids:
                current_app.control.revoke(task_id, terminate=False)
            return HttpResponse(_("Revocation request sent."))
    
        elif action == 'forget':
            CeleryMonitor.get_instance().forget(*task_ids)
            return HttpResponse(_("Forget request sent."))
    
        else:
            return HttpResponseBadRequest(_("Invalid action: %s.") % action)


class TaskLaunchView(IsSuperuserMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs):
        if not is_celery_working():
            return HttpResponseServerError("Celery is not working.")
    
        name = request.POST['name']
        args = shlex.split(request.POST['args'])
        countdown = float(request.POST['countdown'] or '0')

        try:
            task = get_task_by_name(name)
            args, kwargs = convert_task_string_args(task, *args)
            
            result = task.apply_async(args, kwargs, countdown=countdown)
            task_id = result.task_id
            result.forget()
            return HttpResponse(_("Created task %s.") % f"<a href=\"{reverse('zut:celery_task_detail', args=[task_id])}\"><b>{task_id}</b></a>")
        except Exception as err:
            msg = str(err)
            logger.exception(msg)
            return HttpResponseServerError(msg)


class TaskDetailView(IsAuthenticatedMixin, DetailView):
    template_name = 'zut/celery_task_detail.html'

    def get_object(self, queryset = None):        
        id = self.kwargs.get('id')
        info = CeleryMonitor.get_instance().get(id, None)
        if not info:
            info = TaskInfo(id)
        return info
