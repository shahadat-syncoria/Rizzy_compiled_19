from odoo import _, api, fields, models

from werkzeug.urls import url_encode, url_join, url_parse

import logging
import requests

from odoo.exceptions import ValidationError, UserError
from odoo.addons.odoosync_base.utils.app_payment import AppPayment
import json

_logger = logging.getLogger(__name__)

class PaymentProviderClover(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('clover_checkout', "Clover Checkout")], ondelete={'clover_checkout': 'set default'})

    clover_public_api_key = fields.Char(string="Public API key", groups='base.group_system')
        # return response
