class PaymentError(Exception):
    """
    Generic Exception class for all Exceptions related to payments.
    """
    pass


class TransactionDeclined(PaymentError):
    """
    Exception for when transaction has been declined by cybersource.
    """
    pass


class GatewayError(PaymentError):
    """
    Generic Exception class for all Exceptions related to Gateway Error.
    """
    pass


class InvalidGatewayRequestError(PaymentError):
    """
    The GatewayRequest was
    """
    pass


class InsufficientPaymentSources(PaymentError):
    """
    Exception for when a user attempts to checkout without specifying enough
    payment sources to cover the entire order total.

    Eg. When selecting an allocation off a giftcard but not specifying a
    bankcard to take the remainder from.
    """
    pass


class RedirectRequired(PaymentError):
    """
    Exception to be used when payment processing requires a redirect
    """

    def __init__(self, url):
        self.url = url


class UnableToTakePayment(PaymentError):
    """
    Exception to be used for ANTICIPATED payment errors (eg card number wrong,
    expiry date has passed).  The message passed here will be shown to the end
    user.
    """
    pass


class ProcessorMisconfiguredError(Exception):
    """ Raised when a payment processor has invalid/missing settings. """
    pass


class ProcessorNotFoundError(Exception):
    """Raised when a requested payment processor cannot be found."""
    pass


class InvalidSignatureError(GatewayError):
    """The signature of the payment processor's response is invalid."""
    pass


class InvalidCybersourceDecision(GatewayError):
    """The decision returned by CyberSource was not recognized."""
    pass


class DuplicateReferenceNumber(PaymentError):
    """
    CyberSource returned an error response with reason code 104, indicating that
    a duplicate reference number (i.e., order number) was received in a 15 minute period.

    See https://support.cybersource.com/cybskb/index?page=content&id=C156&pmv=print.
    """
    pass


class PartialAuthorizationError(PaymentError):
    """The amount authorized by the payment processor differs from the requested amount."""
    pass


class PCIViolation(PaymentError):
    """ Raised when a payment request violates PCI compliance.

    If we are raising this exception BAD things are happening, and the service MUST be taken offline IMMEDIATELY!
    """
    pass

