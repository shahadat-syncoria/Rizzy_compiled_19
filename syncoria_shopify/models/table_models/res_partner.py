# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _

import pprint
import json

from odoo import exceptions
from ...shopify.utils import *
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    shopify_latitude = fields.Char(
        string='Latitude',
    )

    shopify_longitude = fields.Char(
        string='Longitude',
    )

    shopify_id = fields.Char(string="Shopify ID",
                             store=True
                             # readonly=True,
                             )

    shopify_add_id = fields.Char(string="Address id",
                             store=True,
                             readonly=True,
                             )

    shopify_warehouse_id = fields.Char(string="Shopify Warehouse ID",
                                 store=True,
                                 readonly=True,
                                 )

    shopify_warehouse_active = fields.Boolean(string="Shopify Warehouse Active")

    shopify_accepts_marketing = fields.Boolean(
        string='Email Marketing',
        default=False,
    )

    shopify_last_order_id = fields.Char(string="Last Order Id", readonly=True)

    shopify_last_order_name = fields.Char(string="Last Order Name", readonly=True)

    marketing_opt_in_level = fields.Selection(
        string='field_name',
        selection=[('single_opt_in', 'single_opt_in'), ('confirmed_opt_in', 'confirmed_opt_in'),('unknown','unknown')],
        readonly=True,
    )

    multipass_identifier = fields.Char(string="Multi Pass Identifier", readonly=True)

    orders_count = fields.Integer(
        string='Orders Count',
    )

    shopify_state = fields.Selection(
        string='Shopify Status',
        selection=[('disabled', 'Disabled'), ('invited', 'Invited'),('enabled','Enabled'),('declined','Declined')],
    )

    shopify_tax_settings = fields.One2many(
        string='Tax Settings',
        comodel_name='shopify.tax.settings',
        inverse_name='partner_id',
        readonly=True,
    )

    shopify_tax_exempt = fields.Boolean(
        string='Tax Exempt',
        default=False,
        readonly=True,
    )

    shopify_tax_exemptions_ids = fields.One2many(
        string='Shopify Tax Exemptions',
        comodel_name='shopify.tax.exemptions',
        inverse_name='partner_id',
        readonly=True,
    )

    shopify_total_spent = fields.Monetary(string="Total Spent", readonly=True)

    shopify_verified_email = fields.Boolean(
        string='Verified Email',
        default=False,
        readonly=True,
    )

    shopify_default = fields.Boolean(default=False)

    shopify_company_name = fields.Char(string="Shopify Contact Company Name")

    ##############Should not delete from Shopify####################################
    # def unlink(self):
    #     for rec in self:
    #         if rec.marketplace_type == 'shopify' and rec.shopify_id != 0:
    #             response = shopify_add_req(rec,{},'delete')
    #             response = json.loads(response)
    #             _logger.info("response==>>>" +  str(response))
    #         result = super(ResPartner, rec).unlink()
    #     return result
    ##############Should not delete from Shopify####################################


class ShopifyTaxSettings(models.Model):
    _name = 'shopify.tax.settings'

    _description = 'Shopify Tax Settings'

    _rec_name = 'name'

    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )

    partner_id = fields.Many2one(
        string='partner',
        comodel_name='res.partner',
        ondelete='restrict',
    )

class ShopifyTaxExemptions(models.Model):
    _name = 'shopify.tax.exemptions'

    _description = 'Shopify TAx Exemptions'

    _rec_name = 'name'

    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )

    partner_id = fields.Many2one(
        string='partner',
        comodel_name='res.partner',
        ondelete='restrict',
    )
