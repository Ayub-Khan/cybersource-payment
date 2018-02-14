from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField


@python_2_unicode_compatible
class AbstractTransaction(models.Model):
    """
    A transaction for a particular payment event.
    """
    AUTHORISE, DEBIT, REFUND = 'Authorise', 'Debit', 'Refund'
    txn_type = models.CharField(_("Type"), max_length=128, blank=True)

    amount = models.DecimalField(_("Amount"), decimal_places=2, max_digits=12)
    reference = models.CharField(_("Reference"), max_length=128, blank=True)
    status = models.CharField(_("Status"), max_length=128, blank=True)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    def __str__(self):
        return _(u"%(type)s of %(amount).2f") % {
            'type': self.txn_type,
            'amount': self.amount}

    class Meta:
        abstract = True
        # app_label = 'cybersource-payment'
        ordering = ['-date_created']
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")


@python_2_unicode_compatible
class AbstractPaymentProcessorResponse(models.Model):
    """
    Auditing model used to save all responses received from payment processors.
    """
    transaction_id = models.CharField(_('Transaction ID'), max_length=255, null=True, blank=True)
    reference = models.CharField(_("Reference"), max_length=128, blank=True)
    response = JSONField()
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    class Meta(object):
        ordering = ['-date_created']
        verbose_name = _('Payment Processor Response')
        verbose_name_plural = _('Payment Processor Responses')
