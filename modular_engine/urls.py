from django.urls import path
from . import views


urlpatterns = [
    path('module/', views.module_list, name='module_list'),
    path('module/install/<str:module_name>/', views.install, name='install_module'),
    path('module/uninstall/<str:module_name>/', views.uninstall, name='uninstall_module'),
    path('module/upgrade/<str:module_name>/', views.upgrade, name='upgrade_module'),
]