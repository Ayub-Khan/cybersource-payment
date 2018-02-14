from . import abstract_models
from .utils import is_model_registered


__all__ = []


if not is_model_registered('cybersource-payment', 'Transaction'):
    class Transaction(abstract_models.AbstractTransaction):
        pass

    __all__.append('Transaction')


if not is_model_registered('cybersource-payment', 'AbstractPaymentProcessorResponse'):
    class PaymentProcessorResponse(abstract_models.AbstractPaymentProcessorResponse):
        pass

    __all__.append('PaymentProcessorResponse')
