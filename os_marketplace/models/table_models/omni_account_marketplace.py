# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import api, fields, models
import logging


_logger = logging.getLogger(__name__)


class OmniAccountMarketplace(models.Model):
    _inherit = "omni.account"

    marketplace_ids = fields.One2many(
        string="Marketplace",
        comodel_name="marketplace.instance",
        inverse_name="account_id",
    )
