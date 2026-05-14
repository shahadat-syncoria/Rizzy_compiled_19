# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import fields, models, api, _
import requests

import logging
_logger = logging.getLogger(__name__)


class PosOrderInherit(models.Model):
    _inherit = 'pos.order'

    clover_request_id = fields.Char("Clover Request ID")

    clover_ext_payment_ids = fields.Char("Clover External Payment Ids")

    clover_last_action = fields.Char("Clover Last Action")
