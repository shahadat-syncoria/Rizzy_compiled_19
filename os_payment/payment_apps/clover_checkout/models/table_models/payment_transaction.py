# -*- coding: utf-8 -*-

import logging

from werkzeug import urls

from odoo import _, api, models, fields
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare
from odoo.addons.payment import utils as payment_utils
import pprint
import json
from odoo.addons.payment import utils as payment_utils
import requests

# from odoo.odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CloverPaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    clover_checkout_reference = fields.Char('clover Checkout Reference')

    clover_checkout_merchant_transaction_id = fields.Char('Clover Checkout Merchant Transaction Id')

    clover_checkout_merchant_id = fields.Char('Clover Checkout Merchant Id')

    clover_checkout_refund_status = fields.Char()

    clover_checkout_id = fields.Char()

    clover_data_id = fields.Char()
