# -*- coding: utf-8 -*-
# © Syncoria Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# Module: payment_globalpay
# This module contains functionality for interacting with the GlobalPay API,

import hashlib
import hmac
import logging
import pprint
import requests
import six
from werkzeug.urls import url_join
from odoo import  api, fields, models
from odoo.exceptions import ValidationError,UserError
import base64
import json
from datetime import datetime
from odoo.addons.odoosync_base.utils.app_payment import AppPayment


_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('globalpay', "GlobalPay")], ondelete={'globalpay': 'set default'})
