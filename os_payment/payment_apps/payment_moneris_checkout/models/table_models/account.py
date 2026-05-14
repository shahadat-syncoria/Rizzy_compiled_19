# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api
from odoo.http import request
from odoo.exceptions import UserError
import logging
import pprint
import json
_logger = logging.getLogger(__name__)


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    moneris_move_name = fields.Char()

    payment_type_inbound = fields.Boolean()

    payment_type_outbound = fields.Boolean()
