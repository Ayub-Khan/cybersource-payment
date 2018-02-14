from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CybersourcePaymentConfig(AppConfig):
    label = 'cybersource-payment'
    name = 'cybersource-payment'
    verbose_name = _('Cybersource Payment')
