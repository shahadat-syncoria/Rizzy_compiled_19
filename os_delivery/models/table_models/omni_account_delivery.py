# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import api, fields, models
import logging


_logger = logging.getLogger(__name__)


class OmniAccountDelivery(models.Model):
    _inherit = "omni.account"

    carrier_ids = fields.One2many(
        string="Delivery Carriers",
        comodel_name="delivery.carrier",
        inverse_name="account_id",
    )
