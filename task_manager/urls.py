from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # app inicio
    path("", include("manager.urls")),
    # app tareas
    path("", include("tasks.urls")),
]
