# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import base64
import json
from odoo.http import request
from odoo import api, exceptions, fields, models
from odoo.addons.payment.models.payment_provider import ValidationError
from odoo.addons.odoosync_base.utils.app_payment import AppPayment
import requests
import logging
import string
import random
import re
import urllib
from urllib.parse import unquote
from odoo.service import common

version_info = common.exp_version()
server_serie = version_info.get('server_serie')

_logger = logging.getLogger(__name__)



class providerbambora(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('bamborachk', 'Bambora Checkout')],
        ondelete={'bamborachk': 'set default'})

    bamborachk_transaction_type = fields.Selection(
        string=("Transaction Type"),
        selection=[('purchase', ('Purchase'))], default='purchase')

    bamborachk_merchant_id = fields.Char(string='Merchant ID')

    bamborachk_payment_api = fields.Char(string='Payment API')

    bamborachk_profile_api = fields.Char(string='Profile API')

    bamborachk_order_confirmation = fields.Selection(string='Order Confirmation', selection=[
        ('capture', ('Authorize & capture the amount and conform it'))], default='capture')

    fees_active = fields.Boolean(default=False)

    fees_dom_fixed = fields.Float(default=0.35)

    fees_dom_var = fields.Float(default=3.4)

    fees_int_fixed = fields.Float(default=0.35)

    fees_int_var = fields.Float(default=3.9)
