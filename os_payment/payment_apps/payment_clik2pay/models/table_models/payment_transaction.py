# -*- coding: utf-8 -*-

import logging

from werkzeug import urls

from odoo import  api, models, fields
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
from odoo.addons.payment import utils as payment_utils
import pprint
import json
from odoo.addons.payment import utils as payment_utils
import requests

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    clik2pay_reference = fields.Char('Clik2Pay Reference')

    clik2pay_merchant_transaction_id = fields.Char('Clik2Pay Merchant Transaction Id')

    clik2pay_merchant_id = fields.Char('Clik2Pay Merchant Id')

    click2pay_refund_status = fields.Char()

    demo_success_failed = fields.Selection([('PAID', 'Success'), ('CANCELLED', 'Failed')])
