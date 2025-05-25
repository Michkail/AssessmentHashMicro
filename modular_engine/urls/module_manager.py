# File: modular_engine/urls/module_manager.py
from django.urls import path
from modular_engine.views.module_manager import module_manager_view


urlpatterns = [
    path("", module_manager_view, name="module_manager"),
]
