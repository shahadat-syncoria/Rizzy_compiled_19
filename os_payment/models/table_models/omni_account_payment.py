# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo.addons.odoosync_base.utils.helper import image_processing
from odoo import api, fields, models

import requests
import logging

_logger = logging.getLogger(__name__)


class OmniAccountPayment(models.Model):
    _inherit = "omni.account"

    provider_ids = fields.One2many(
        string="Payment providers",
        comodel_name="payment.provider",
        inverse_name="account_id",
    )

    journal_ids = fields.One2many(
        string="Account Journals",
        comodel_name="account.journal",
        inverse_name="account_id"
    )
