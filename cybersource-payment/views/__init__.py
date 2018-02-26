import abc
import logging

import six
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, View
from ..utils import get_model  # Todo: use the app path instead of relative

from blah.blah.blah import redirect_url

logger = logging.getLogger(__name__)


class PaymentFailedView(TemplateView):
    template_name = 'payment/payment_error.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentFailedView, self).get_context_data(**kwargs)
        context.update({
            'dashboard_url': dashboard_url,  # Todo: update to correct url
            # Might be removing if no support email
            'payment_support_email': self.request.site.siteconfiguration.payment_support_email
        })
        return context


class BasePaymentSubmitView(View):
    """ Base class for payment submission views.

    Client-side payment processors should implement a view with this base class. The front-end should POST
    to this view where finalization of payment and order creation will be handled.
    """
    form_class = PaymentForm
    http_method_names = ['post', 'options']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        logger.info(
            '%s called for basket [%d]. It is in the [%s] state.',
            self.__class__.__name__,
            request.basket.id,
            request.basket.status
        )
        return super(BasePaymentSubmitView, self).dispatch(request, *args, **kwargs)

    def post(self, request):  # pylint: disable=unused-argument
        # NOTE (CCB): Ideally, we'd inherit FormView; however, doing so causes issues for children
        # of this class that want to inherit mixins (e.g. EdxOrderPlacementMixin).
        form_kwargs = self.get_form_kwargs()
        form = self.form_class(**form_kwargs)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        return {
            'data': self.request.POST,
            'user': self.request.user,
            'request': self.request,
        }

    @abc.abstractmethod
    def form_valid(self, form):
        """ Perform payment processing after validating the form submission. """

    def form_invalid(self, form):
        logger.info(
            'Invalid payment form submitted for basket [%d].',
            self.request.basket.id
        )

        errors = {field: error[0] for field, error in six.iteritems(form.errors)}
        logger.debug(errors)

        data = {'field_errors': errors}

        if errors.get('basket'):
            data['error'] = _('There was a problem retrieving your basket. Refresh the page to try again.')

        return JsonResponse(data, status=400)