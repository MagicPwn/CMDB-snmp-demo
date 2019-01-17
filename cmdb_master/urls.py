from django.urls import path

from .views import *
import xadmin
xadmin.autodiscover()
urlpatterns = [
#    path('task/<str:taskid>/run/', run, name='run'),
#    path('task/<str:taskid>/data/', taskData, name='taskData'),
#    path('container/<str:containerid>/log/', get_log, name='containerlog'),
#    path('container/<str:containerid>/console/', get_console, name='containerconsole'),
#    path('tool/<str:toolid>/console/', get_console_chat, name='containerconsole'),
#    path('tool/<str:tool_id>/pull-compile/', create_tool, name='containercompile'),
#    path('<str:typeofm>/download/<str:instance_id>', file_down, name='filedown'),
#    path('<str:typeofm>/choice/<str:instance_id>', file_choice, name='filechoice'),
#    path('<str:typeofm>/upload/<str:instance_id>', file_upload, name='fileup'),
#    path('Policy/set_condition/', create_policy, name='create_policy'),
    path('', xadmin.site.urls),  # 前台
    path('on_watch', on_watch),  # 前台
]