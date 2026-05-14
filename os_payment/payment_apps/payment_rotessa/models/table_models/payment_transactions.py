import logging
from datetime import datetime

from odoo import fields,api,models
from odoo.exceptions import UserError
from odoo.http import request
from odoo.addons.payment import utils as payment_utils
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class RotessaTransactions(models.Model):
    _inherit='payment.transaction'

    rotessa_track_id = fields.Many2one('rotessa.transaction.tracking')

        # self._finalize_post_processing()

        # self.provider_reference = response_content.get('x_trans_id')
        # status_code = response_content.get('x_response_code', '3')
        # if status_code == '1':  # Approved
        #     status_type = response_content.get('x_type').lower()
        #     if status_type in ('auth_capture', 'prior_auth_capture'):
        #         self._set_done()
        #         if self.tokenize and not self.token_id:
        #             self._authorize_tokenize()
        #     elif status_type == 'auth_only':
        #         self._set_authorized()
        #         if self.tokenize and not self.token_id:
        #             self._authorize_tokenize()
        #         if self.operation == 'validation':
        #             self._send_void_request()  # In last step because it processes the response.
        #     elif status_type == 'void':
        #         if self.operation == 'validation':  # Validation txs are authorized and then voided
        #             self._set_done()  # If the refund went through, the validation tx is confirmed
        #         else:
        #             self._set_canceled()
        #     elif status_type == 'refund' and self.operation == 'refund':
        #         self._set_done()
        #         # Immediately post-process the transaction as the post-processing will not be
        #         # triggered by a customer browsing the transaction from the portal.
        #         self.env.memo('payment.cron_post_process_payment_tx')._trigger()
        # elif status_code == '2':  # Declined
        #     self._set_canceled()
        # elif status_code == '4':  # Held for Review
        #     self._set_pending()
        # else:  # Error / Unknown code
        #     error_code = response_content.get('x_response_reason_text')
        #     _logger.info(
        #         "received data with invalid status (%(status)s) and error code (%(err)s) for "
        #         "transaction with reference %(memo)s",
        #         {
        #             'status': status_code,
        #             'err': error_code,
        #             'memo': self.reference,
        #         },
        #     )
        #     self._set_error(
        #         "Authorize.Net: " + (
        #             "Received data with status code \"%(status)s\" and error code \"%(error)s\"",
        #             status=status_code, error=error_code
        #         )
        #     )
