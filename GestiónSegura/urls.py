"""
URL configuration for GestiónSegura project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clientes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/<int:cliente_id>/', views.cliente_details, name='cliente_details'),
    path('clientes/<int:cliente_id>/edit/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:cliente_id>/delete/', views.delete_cliente, name='delete_cliente'),
    path('clientes/<int:cliente_id>/añadir/', views.añadir_poliza, name='añadir_poliza'),
    path('clientes/<int:cliente_id>/<int:poliza_id>/edit/', views.editar_poliza, name='editar_poliza'),
    path('clientes/<int:cliente_id>/<int:poliza_id>/delete/', views.delete_poliza, name='delete_poliza'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
]
