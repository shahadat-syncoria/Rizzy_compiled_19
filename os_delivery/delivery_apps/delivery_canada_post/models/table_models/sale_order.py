# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    canadapost_certificate_number = fields.Char(string="Certificate Number")

    canadapost_licence_number = fields.Char(string="Licence Number")

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    canadapost_service = fields.Char(string="canadapost Service")

    canadapost_domestic_sale = fields.Boolean(string='Domestic Sale?', 
        compute='_compute_domestic_sale')

    @api.depends('partner_shipping_id')
    def _compute_domestic_sale(self):
        for record in self:
            record.canadapost_domestic_sale = False
            if record.partner_shipping_id.country_id:
                if record.partner_shipping_id.country_id.id == record.company_id.country_id.id:
                    record.canadapost_domestic_sale = True

    canadapost_export_reason = fields.Selection(
        string='Export Reason',
        selection=[('DOC', 'document'), 
                    ('SAM', 'Commercial Sample'),
                    ('REP', 'Repair or warranty'),
                    ('SOG', 'Sale of Goods'),
                    ('OTH', 'Other')],default='SOG')

    canadapost_other_reason = fields.Char(string='Other Reason')



class ProductProduct(models.Model):
    _inherit = 'product.product'

    country_of_origin = fields.Many2one(
        string='Origin Country',
        comodel_name='res.country',
        ondelete='restrict',
    )

    province_of_origin = fields.Many2one(
        string='Origin Province',
        comodel_name='res.country.state',
        ondelete='restrict',
        domain="[('country_id', '=', country_of_origin)]"
    )  
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    country_of_origin = fields.Many2one(
        string='Origin Country',
        comodel_name='res.country',
        ondelete='restrict',
    )

    province_of_origin = fields.Many2one(
        string='Origin Province',
        comodel_name='res.country.state',
        ondelete='restrict',
        domain="[('country_id', '=', country_of_origin)]"
    )
