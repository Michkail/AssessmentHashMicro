from django.shortcuts import render, redirect
from .models import Module
from .services import get_available_modules, install_module, uninstall_module, upgrade_module


def module_list(request):
    available = get_available_modules()
    installed = Module.objects.filter(status='installed')
    return render(request, 'modular_engine/module_list.html', {'available': available, 'installed': installed})

def install(request, module_name):
    install_module(module_name)
    return redirect('module_list')

def uninstall(request, module_name):
    uninstall_module(module_name)
    return redirect('module_list')

def upgrade(request, module_name):
    upgrade_module(module_name)
    return redirect('module_list')