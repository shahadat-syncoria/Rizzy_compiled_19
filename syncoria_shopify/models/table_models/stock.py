# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import pprint
import re
from ...shopify.utils import *
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)
from odoo import exceptions


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    shopify_id = fields.Char(string="Fulfillment ID", copy=False)

    shopify_order_id = fields.Char(string="Shopify Order ID", related='sale_id.shopify_id')

    shopify_status = fields.Char(copy=False, string='Shipment Status')

    shopify_service = fields.Char(copy=False, string='Shopify Service')

    shopify_track_updated = fields.Boolean(default=False, readonly=True, copy=False)

    shopify_tracking_urls = fields.Char(string="Shopify Tracking Url", copy=False)

    shopify_tracking_company = fields.Char(string="Shopify Tracking Company", copy=False)

    shopify_location_id = fields.Char(string='Shopify Location ID')

    shopify_tracking_number = fields.Char(string='Shopify Tracking Number')


class InheritedStockLocation(models.Model):
    _inherit = 'stock.location'

    shopify_warehouse_ids = fields.Many2many("shopify.warehouse",string="Shopify Warehouse")


# class InheritedStockWarehouse(models.Model):
#     _inherit = 'stock.warehouse'
#
#     shopify_location_id = fields.Many2one("shopify.warehouse", string="Shopify Warehouse")
#     shopify_invent_id = fields.Char("Shopify Location ID", related="shopify_location_id.shopify_invent_id")
#
#     _sql_constraints = [
#         ('shopify_location_id', 'unique (shopify_location_id)', 'Only 1 odoo map 1 shopify location.'),
#     ]


class InheritedStockMove(models.Model):
    _inherit = 'stock.move'
