import requests
from odoo import api, fields, models,_

import  logging
_logger = logging.getLogger(__name__)

class OmniAccountPosPayment(models.Model):
    _inherit = "omni.account"

    pos_payment_methods_ids = fields.One2many(
        string="POS Payment Methods",
        comodel_name="pos.payment.method",
        inverse_name="account_id"
    )
