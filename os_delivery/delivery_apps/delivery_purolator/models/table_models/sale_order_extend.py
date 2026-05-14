# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purolator_service = fields.Char()

class ProductProduct(models.Model):
    _inherit = 'product.product'

    country_of_manufacture = fields.Many2one('res.country', string='Country of Manufacture')

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    country_of_manufacture = fields.Many2one('res.country', string='Country of Manufacture')
