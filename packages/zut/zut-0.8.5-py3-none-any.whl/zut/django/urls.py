from django.urls import path
from . import views

try:
    from .celery import views as celery_views, websockets as celery_websockets
except ImportError:
    celery_views = None
    celery_websockets = None

app_name = 'zut'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('lang/', views.LangView.as_view(), name='lang'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

if celery_views:
    urlpatterns += [
        path('task/', celery_views.TaskListView.as_view(), name='celery_task_list'),
        path('task/launch/', celery_views.TaskLaunchView.as_view(), name='celery_task_launch'),
        path('task/<uuid:id>/', celery_views.TaskDetailView.as_view(), name='celery_task_detail'),
    ]


websocket_urlpatterns = []

if celery_websockets:
    websocket_urlpatterns += [
        path('task/', celery_websockets.TaskListWebsocket.as_asgi()),
        path('task/<uuid:id>/', celery_websockets.TaskDetailWebsocket.as_asgi()),
    ]
