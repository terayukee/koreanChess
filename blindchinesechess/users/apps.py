from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "blindchinesechess.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import blindchinesechess.users.signals  # noqa: F401
        except ImportError:
            pass


# class UsersConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'users'