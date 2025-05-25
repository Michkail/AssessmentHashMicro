import importlib
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.urls import include, path
from django.utils.module_loading import import_module

MODULES_DIR = settings.BASE_DIR / 'modules'


def get_available_modules():
    if not MODULES_DIR.exists():
        return []
    
    return [d.name for d in MODULES_DIR.iterdir()
            if d.is_dir() and (d / '__init__.py').exists()]


def install_module(module_name):
    module_path = MODULES_DIR / module_name
    
    if not module_path.exists():
        raise Exception(f"Module '{module_name}' not found in modules directory")

    full_module_path = f"modules.{module_name}"

    if full_module_path not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS += (full_module_path,)

    try:
        model_module = importlib.import_module(f"modules.{module_name}.models")

        for attr_name in dir(model_module):
            attr = getattr(model_module, attr_name)

            if hasattr(attr, '_meta') and hasattr(attr._meta, 'app_label'):
                setup_roles_and_permissions(attr)

    except ModuleNotFoundError:
        pass



def uninstall_module(module_name):
    full_module_path = f"modules.{module_name}"

    if full_module_path in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS = tuple(app for app in settings.INSTALLED_APPS if app != full_module_path)


def upgrade_module(module_name):
    full_module_path = f"modules.{module_name}"
    call_command('makemigrations', full_module_path)
    call_command('migrate', full_module_path)

    try:
        model_module = importlib.import_module(f"modules.{module_name}.models")

        for attr_name in dir(model_module):
            attr = getattr(model_module, attr_name)

            if hasattr(attr, '_meta') and hasattr(attr._meta, 'app_label'):
                setup_roles_and_permissions(attr)

    except ModuleNotFoundError:
        pass


def get_dynamic_module_urls():
    urlpatterns = []

    for module_name in get_available_modules():
        full_module_path = f"modules.{module_name}"

        if full_module_path not in settings.INSTALLED_APPS:
            continue

        try:
            module_urls = import_module(f"modules.{module_name}.urls")
            urlpatterns.append(path(f"{module_name}/", include(module_urls)))

        except ModuleNotFoundError:
            continue

    return urlpatterns


def setup_roles_and_permissions(model_class):
    content_type = ContentType.objects.get_for_model(model_class)

    manager_group, _ = Group.objects.get_or_create(name="manager")
    user_group, _ = Group.objects.get_or_create(name="user")
    public_group, _ = Group.objects.get_or_create(name="public")

    perms = Permission.objects.filter(content_type=content_type)
    perm_dict = {p.codename: p for p in perms}

    manager_perms = ['add', 'change', 'delete', 'view']
    user_perms = ['add', 'change', 'view']
    public_perms = ['view']

    for codename in manager_perms:
        perm = perm_dict.get(f"{codename}_{model_class._meta.model_name}")
        if perm: manager_group.permissions.add(perm)

    for codename in user_perms:
        perm = perm_dict.get(f"{codename}_{model_class._meta.model_name}")
        if perm: user_group.permissions.add(perm)

    for codename in public_perms:
        perm = perm_dict.get(f"{codename}_{model_class._meta.model_name}")
        if perm: public_group.permissions.add(perm)

