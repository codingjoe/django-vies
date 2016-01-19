from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ViesConfig(AppConfig):
    name = 'vies'
    verbose_name = _("Vies")
    allow_server_error = True


class ViesDisallowServerErrorConfig(ViesConfig):
    allow_server_error = False
