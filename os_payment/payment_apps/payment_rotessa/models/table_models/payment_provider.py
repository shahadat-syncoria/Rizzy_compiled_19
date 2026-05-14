import json
import logging
import pprint

import requests

from odoo import  api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.addons.odoosync_base.utils.app_payment import AppPayment

_logger = logging.getLogger(__name__)


class PaymentProviderRotessa(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('rotessa', "Rotessa")], ondelete={'rotessa': 'set default'})

    test_transaction_schedule_id = fields.Char("Test Transaction Schedule ID")
