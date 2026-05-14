import base64
import json
import logging

import requests

from odoo import fields, models, SUPERUSER_ID

_logger = logging.getLogger(__name__)


class ShopifyProductMappings(models.Model):
    _name = 'shopify.product.mappings'

    name = fields.Char('Name')

    shopify_instance_id = fields.Many2one("marketplace.instance", string="Shopify Instance ID", required=True, )

    product_id = fields.Many2one("product.product", string="Product", )

    product_tmpl_id = fields.Many2one("product.template", string="Product Template", related='product_id.product_tmpl_id',)

    shopify_id = fields.Char(string="Shopify Variant Id", copy=False, required=True, )

    shopify_parent_id = fields.Char(string="Shopify Product Id", copy=False, )

    shopify_inventory_id = fields.Char(string="Shopify Inventory Id", copy=False, required=True, )

    default_code = fields.Char(string="SKU", related='product_id.default_code', store=True)

    _sql_constraints = [
        (
            'unique_shopifyinstance_byshopifyid',
            'UNIQUE(shopify_instance_id, shopify_id)',
            'Only one instance exist only one shopify id.',
        )
    ]
