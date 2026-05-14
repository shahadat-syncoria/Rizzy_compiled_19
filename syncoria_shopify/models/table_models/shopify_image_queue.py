# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
import base64
import json
import logging
import requests

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ShopifyImageQueue(models.Model):
    _name = 'shopify.image.queue'

    _description = 'Shopify Image Queue'

    _order = 'create_date desc, id desc'

    shopify_instance_id = fields.Many2one(
        'marketplace.instance',
        string='Shopify Instance',
        required=True,
        ondelete='cascade',
    )

    shopify_image_id = fields.Char(string='Image ID')

    product_id = fields.Char(string='Product ID')

    position = fields.Integer(string='Position', default=1)

    src = fields.Char(string='Source URL')

    variant_ids = fields.Char(string='Variant IDs', help='JSON array of variant IDs')

    state = fields.Selection([
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    ], string='State', default='pending', required=True, index=True)
