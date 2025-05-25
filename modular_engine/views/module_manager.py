from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from modular_engine.services import (get_available_modules, install_module,
                                     uninstall_module, upgrade_module)


def module_manager_view(request):
    modules = get_available_modules()
    installed_modules = [app.split('.')[-1]
                         for app in settings.INSTALLED_APPS
                         if app.startswith("modules.")]

    if request.method == "POST":
        action = request.POST.get("action")
        module_name = request.POST.get("module_name")

        try:
            if action == "install":
                install_module(module_name)
                messages.success(request, f"Module '{module_name}' installed.")

            elif action == "upgrade":
                upgrade_module(module_name)
                messages.success(request, f"Module '{module_name}' upgraded.")

            elif action == "uninstall":
                uninstall_module(module_name)
                messages.success(request, f"Module '{module_name}' uninstalled.")

        except Exception as e:
            messages.error(request, str(e))

        return redirect("modular_engine:module_manager")

    context = {
        "modules": modules,
        "installed_modules": installed_modules,
    }

    return render(request, "modular_engine/module_manager.html", context)
