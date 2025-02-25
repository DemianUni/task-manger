from django.urls import path
from . import views

urlpatterns = [
    path("tasks-list/", views.tasks_list, name="tasks_list"),
    path("create/", views.task_create, name="task_create"),
    path("edit/<int:pk>/", views.task_edit, name="task_edit"),
    path("delete/<int:pk>/", views.task_delete, name="task_delete"),
    # de
    path("create-weeklytask/", views.WeeklyTask_create, name="WeeklyTask_create"),
    path("edit-weeklytask/<int:pk>/", views.weeklytask_edit, name="weeklytask_edit"),
    path(
        "delete-weeklytask/<int:pk>/",
        views.weeklytask_delete,
        name="weeklytask_delete",
    ),
    # gantt
    path("gantt/", views.gantt_chart, name="gantt_chart"),
    path("not/", views.notifications_view, name="not"),
]
