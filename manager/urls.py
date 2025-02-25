from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("menu")),  # Redirigir a menu
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("menu/", views.menu, name="menu"),
    # Otros patrones de URL
    path(
        "resultados-año-pasado/",
        views.resultados_año_pasado,
        name="resultados_año_pasado",
    ),
    path("agregar-general/", views.agregar_general, name="agregar_general"),
    path("agregar-alianza/", views.agregar_alianza, name="agregar_alianza"),
    path("editar-general/<int:pk>/", views.editar_general, name="editar_general"),
    path("eliminar-general/<int:pk>/", views.eliminar_general, name="eliminar_general"),
    path("editar-alianza/<int:pk>/", views.editar_alianza, name="editar_alianza"),
    path("eliminar-alianza/<int:pk>/", views.eliminar_alianza, name="eliminar_alianza"),
    path(
        "proyectos-año-presente/",
        views.proyectos_año_presente,
        name="proyectos_año_presente",
    ),
    # Estadistica Informacion
    path(
        "estadistica-informacion/",
        views.estadistica_informacion,
        name="estadistica_informacion",
    ),
    path(
        "agregar-estadistica-informacion/",
        views.agregar_estadistica_informacion,
        name="agregar_estadistica_informacion",
    ),
    path(
        "editar-estadistica-informacion/<int:pk>/",
        views.editar_estadistica_informacion,
        name="editar_estadistica_informacion",
    ),
    path(
        "eliminar-estadistica-informacion/<int:pk>/",
        views.eliminar_estadistica_informacion,
        name="eliminar_estadistica_informacion",
    ),
    # planeasion Estrategia
    path(
        "planeacion-estrategia/",
        views.planeacion_estrategia,
        name="planeacion_estrategia",
    ),
    path(
        "agregar-planeacion-estrategia/",
        views.agregar_planeacion_estrategia,
        name="agregar_planeacion_estrategia",
    ),
    path(
        "editar-planeacion-estrategia/<int:pk>/",
        views.editar_planeacion_estrategia,
        name="editar_planeacion_estrategia",
    ),
    path(
        "eliminar-planeacion-estrategia/<int:pk>/",
        views.eliminar_planeacion_estrategia,
        name="eliminar_planeacion_estrategia",
    ),
    # Procesos / R
    path("procesos-r/", views.procesos_r, name="procesos_r"),
    path("agregar-procesos-r/", views.agregar_procesos_r, name="agregar_procesos_r"),
    path(
        "editar-procesos-r/<int:pk>/", views.editar_procesos_r, name="editar_procesos_r"
    ),
    path(
        "eliminar-procesos-r/<int:pk>/",
        views.eliminar_procesos_r,
        name="eliminar_procesos_r",
    ),
    # Alianzas
    path("alianzas/", views.alianzas, name="alianzas"),
    path(
        "agregar-alianza-presente/",
        views.agregar_alianza_presente,
        name="agregar_alianza_presente",
    ),
    path(
        "editar-alianza-presente/<int:pk>/",
        views.editar_alianza_presente,
        name="editar_alianza_presente",
    ),
    path(
        "eliminar-alianza-presente/<int:pk>/",
        views.eliminar_alianza_presente,
        name="eliminar_alianza_presente",
    ),
]
