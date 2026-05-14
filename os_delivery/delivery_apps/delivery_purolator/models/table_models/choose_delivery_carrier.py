# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import api, models, fields, _, tools
import logging

_logger = logging.getLogger(__name__)

class ProviderPurolator(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    purolator_shipping_date =  fields.Date(string='Shipping Date', required=True, default=fields.Date.today())

    purolator_total_weight =  fields.Float(string='Total Weight')

    purolator_weight_unit = fields.Selection([('LB', 'LB'), ('KG', 'KG')], default='KG', string="Weight Unit", required=True)

    purolator_service = fields.Char()

    purolator_service_type = fields.Many2one(comodel_name="purolator.service")

    purolator_get_service = fields.Boolean(string='Select Service Options')
        
           
class PurolatorService(models.TransientModel):
    _name = "purolator.service"

    _description = "Purolator Services"

    service_id = fields.Char(string="Service ID")

    shipment_date =  fields.Date()

    expected_delivery_date =  fields.Date()

    expected_transit_days =  fields.Integer()

    surcharges = fields.Float()

    taxes = fields.Float()

    options = fields.Float(string="Optional")

    base_price = fields.Float()

    total_price = fields.Float(string="Display Price")

    order_id = fields.Many2one('sale.order')

    choise_id = fields.Many2one('choose.delivery.carrier')

    active = fields.Boolean(string='Status', default=True)
