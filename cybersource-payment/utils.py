from importlib import import_module

from django.apps import apps
from django.apps.config import MODELS_MODULE_NAME
from django.core.exceptions import AppRegistryNotReady

from .models import PaymentProcessorResponse


def get_model(app_label, model_name):
    """
    Fetches a Django model using the app registry.

    This doesn't require that an app with the given app label exists,
    which makes it safe to call when the registry is being populated.
    All other methods to access models might raise an exception about the
    registry not being ready yet.
    Raises LookupError if model isn't found.
    """
    try:
        return apps.get_model(app_label, model_name)
    except AppRegistryNotReady:
        if apps.apps_ready and not apps.models_ready:
            # If this function is called while `apps.populate()` is
            # loading models, ensure that the module that defines the
            # target model has been imported and try looking the model up
            # in the app registry. This effectively emulates
            # `from path.to.app.models import Model` where we use
            # `Model = get_model('app', 'Model')` instead.
            app_config = apps.get_app_config(app_label)
            # `app_config.import_models()` cannot be used here because it
            # would interfere with `apps.populate()`.
            import_module('%s.%s' % (app_config.name, MODELS_MODULE_NAME))
            # In order to account for case-insensitivity of model_name,
            # look up the model through a private API of the app registry.
            return apps.get_registered_model(app_label, model_name)
        else:
            # This must be a different case (e.g. the model really doesn't
            # exist). We just re-raise the exception.
            raise


def is_model_registered(app_label, model_name):
    """
    Checks whether a given model is registered. This is used to only
    register cybersource-payment models if they aren't overridden.
    """
    try:
        apps.get_registered_model(app_label, model_name)
    except LookupError:
        return False
    else:
        return True


def record_processor_response(response, transaction_id=None, reference=None):
        """
        Save the processor's response to the database for auditing.

        Arguments:
            response (dict): Response received from the payment processor
            transaction_id (string): Identifier for the transaction on the payment processor's servers
            reference (string): Basket associated with the payment event (e.g., being purchased)

        Return
            PaymentProcessorResponse
        """
        payment_processor_response = PaymentProcessorResponse.objects.create(
            transaction_id=transaction_id,
            response=response,
            reference=reference
        )
        payment_processor_response.save()
        return payment_processor_response
