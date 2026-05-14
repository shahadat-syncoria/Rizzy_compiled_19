import hashlib
import hmac
import logging
import pprint
import requests
import six
from werkzeug.urls import url_join
from odoo import  api, fields, models
from odoo.exceptions import ValidationError
import base64
from odoo.addons.odoosync_base.utils.app_payment import AppPayment

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('clik2pay', "Clik2Pay")], ondelete={'clik2pay': 'set default'})

    clik2pay_tampered_payment = fields.Boolean('Accept Tampered Payment', default=True)
