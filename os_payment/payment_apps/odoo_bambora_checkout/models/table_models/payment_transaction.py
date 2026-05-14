# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import logging
import pprint

from odoo import  api, models, fields
from odoo.exceptions import UserError, ValidationError
from odoo.http import request
from odoo.addons.odoosync_base.utils.app_payment import AppPayment
from odoo.addons.payment import utils as payment_utils
_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    bamborachk_auth_code = fields.Char('Auth Code')

    bamborachk_created = fields.Char('Bambora Created on')

    bamborachk_order_number = fields.Char('Order Number')

    bamborachk_txn_type = fields.Char("Transaction Type")

    bamborachk_payment_method = fields.Char("Payment Method")

    bamborachk_card_type = fields.Char("Card Type")

    bamborachk_last_four = fields.Char("Last Four")

    bamborachk_avs_result = fields.Char("AVS Result")

    bamborachk_cvd_result = fields.Char("CVD Result")



class PaymentToken(models.Model):
    _inherit = 'payment.token'

    bamborachk_profile = fields.Char()

    bamborachk_token = fields.Char()

    bamborachk_token_type = fields.Selection(
        string='Token Type',
        selection=[('temporary', 'Temporary'), ('permanent', 'Permanent')])

    provider = fields.Selection(
        string='Provider', related='provider_id.code', readonly=False)

    ###########################################################################################
    ###########################################################################################
