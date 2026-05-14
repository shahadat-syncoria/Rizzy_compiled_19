# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class PosConfig(models.Model):
    _inherit = 'pos.config'

    
    # def _force_http(self):
    #     enforce_https = self.env['ir.config_parameter'].sudo().get_param('point_of_sale.enforce_https')
    #     if not enforce_https and self.payment_method_ids.filtered(lambda pm: pm.use_payment_terminal == 'clover_cloud'):
    #         return True
    #     return super(PosConfig, self)._force_http()
