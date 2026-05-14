# -*- coding: utf-8 -*-
# © Syncoria Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# Module: payment_globalpay
# This module contains functionality for interacting with the GlobalPay API,


import logging

from werkzeug import urls

from odoo import  api, models, fields
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare
from odoo.addons.payment import utils as payment_utils
import pprint
import json
from odoo.addons.payment import utils as payment_utils
import requests

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    globalpay_reference = fields.Char('globalpay Reference')

    globalpay_merchant_transaction_id = fields.Char('globalpay Merchant Transaction Id')

    globalpay_merchant_id = fields.Char('globalpay Merchant Id')

    click2pay_refund_status = fields.Char()

    demo_success_failed = fields.Selection([('CAPTURED', 'Success'), ('DECLINED', 'Failed')])
