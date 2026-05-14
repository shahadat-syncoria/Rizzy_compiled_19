# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import api, models, fields, _


class Providercanadapost(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    canadapost_shipping_date = fields.Date(default=fields.Date.today())

    canadapost_service = fields.Char()

    canadapost_service_type = fields.Many2one(comodel_name="canadapost.service")



class CanadapostService(models.TransientModel):
    _name = "canadapost.service"

    _description = "Canada Post Services"

    service_name = fields.Char()

    service_code = fields.Char()

    service_link = fields.Char()

    shipment_date = fields.Date()

    expected_delivery_date = fields.Date()

    expected_transit_days = fields.Integer()

    surcharges = fields.Float()

    taxes = fields.Float()

    options = fields.Float(string="Optional")

    base_price = fields.Float()

    total_price = fields.Float(string="Display Price")

    order_id = fields.Many2one('sale.order')

    choise_id = fields.Many2one('choose.delivery.carrier')

    active = fields.Boolean(string='Status', default=True)
