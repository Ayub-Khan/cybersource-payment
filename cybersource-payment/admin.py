from pprint import pformat

from django.contrib import admin
from django.utils.html import format_html

from .utils import get_model

PaymentProcessorResponse = get_model('cybersource-payment', 'PaymentProcessorResponse')
Transaction = get_model('cybersource-payment', 'Transaction')


@admin.register(PaymentProcessorResponse)
class PaymentProcessorResponseAdmin(admin.ModelAdmin):
    search_fields = ('id', 'transaction_id', 'reference')
    list_display = ('id', 'transaction_id', 'reference', 'date_created')
    fields = ('transaction_id', 'reference', 'formatted_response')
    readonly_fields = ('transaction_id', 'reference', 'formatted_response')
    show_full_result_count = False

    def formatted_response(self, obj):
        pretty_response = pformat(obj.response)

        # Use format_html() to escape user-provided inputs, avoiding an XSS vulnerability.
        return format_html('<br><br><pre>{}</pre>', pretty_response)

    formatted_response.allow_tags = True


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = ('txn_type',)
    search_fields = ('id', 'txn_type', 'status', 'reference')
    list_display = ('id', 'txn_type', 'reference', 'status', 'amount', 'date_created')
    fields = ('txn_type', 'reference', 'reference', 'amount', 'date_created')
    readonly_fields = ('txn_type', 'reference', 'reference', 'amount', 'date_created')
    show_full_result_count = False

