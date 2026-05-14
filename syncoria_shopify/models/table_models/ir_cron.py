# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo.exceptions import UserError
from odoo import models, fields, api, _


class IrCron(models.Model):
    _inherit = 'ir.cron'

    shopify_stock_limit = fields.Integer(default=10)

    shopify_time_limit = fields.Integer(default=4)
