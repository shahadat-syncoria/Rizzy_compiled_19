# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import json
import requests
import base64
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class ShopifyFeedProducts(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _name = 'shopify.feed.products'

    _description = 'Shopify Feed Products'

    _rec_name = 'title'

    _order = 'name DESC'

    name = fields.Char(
        string='Name',
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('shopify.feed.products'))

    instance_id = fields.Many2one(
        string='Marketplace Instance',
        comodel_name='marketplace.instance',
        ondelete='restrict',
    )

    parent = fields.Boolean(default=False)

    title = fields.Char(copy=False)

    shopify_id = fields.Char(string='Shopify Id', readonly=True)

    inventory_id = fields.Char(string='Inventory Id', readonly=True)

    product_data = fields.Text(
        string='Product Data',
    )

    state = fields.Selection(
        string='State',
        tracking=True,
        selection=[('draft', 'draft'), ('queue', 'Queue'),
                   ('processed', 'Processed'), ('failed', 'Failed')]
    )

    product_id = fields.Many2one(
        string='Product Variant',
        comodel_name='product.product',
        ondelete='restrict',
    )

    product_tmpl_id = fields.Many2one(
        string='Product Template',
        comodel_name='product.template',
        ondelete='restrict',
    )

    barcode = fields.Char()

    default_code = fields.Char('Default Code(SKU)')

    feed_varaint_ids = fields.One2many(
        string='Feed Variants',
        comodel_name='shopify.feed.products',
        inverse_name='parent_id',
    )

    feed_variant_count = fields.Integer(compute="_compute_feed_variant_count")

    @api.depends('feed_varaint_ids')
    def _compute_feed_variant_count(self):
        for record in self:
            record.feed_variant_count = len(record.feed_varaint_ids)

    parent_id = fields.Many2one(
        string='Parent Product',
        comodel_name='shopify.feed.products',
        domain=[('parent','=',True)]
    )

    parent_title = fields.Char()

    """ PRODUCT SYNC """
