# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
import json
from locale import currency
from odoo import models, fields, exceptions, api, _, Command
import re
import logging
from ...shopify.utils import to_shopify_gid

_logger = logging.getLogger(__name__)


class SaleOrderShopify(models.Model):
    _inherit = 'sale.order'

    shopify_id = fields.Char(string="Shopify Id", readonly=True,
                             store=True)

    shopify_order = fields.Char(readonly=True, store=True)

    shopify_status = fields.Char(string="shopify status", readonly=True)

    shopify_order_date = fields.Datetime(string="shopify Order Date")

    shopify_carrier_service = fields.Char(string="shopify Carrier Service")

    shopify_has_delivery = fields.Boolean(readonly=True, default=False, compute='shopifyhasdelviery')

    shopify_browser_ip = fields.Char(string='Browser IP', )

    shopify_buyer_accepts_marketing = fields.Boolean('Buyer Accepts Merketing', )

    shopify_cancel_reason = fields.Char('Cancel Reason', )

    shopify_cancelled_at = fields.Datetime('Cancel At', )

    shopify_cart_token = fields.Char('Cart Token', )

    shopify_checkout_token = fields.Char('Checkout Token', )

    shopify_currency = fields.Many2one(
        string='Shop Currency',
        comodel_name='res.currency',
        ondelete='restrict',
    )

    shopify_financial_status = fields.Selection(
        string='Financial Status',
        selection=[('pending', 'Pending'),
                   ('authorized', 'Authorized'),
                   ('partially_paid', 'Partially Paid'),
                   ('paid', 'Paid'),
                   ('partially_refunded', 'Partially Refunded'),
                   ('voided', 'Voided'),
                   ('refunded', 'Refunded')
                   ], default='pending'

    )

    shopify_fulfillment_status = fields.Char('Fullfillment Status', )

    shopify_track_updated = fields.Boolean(default=False, readonly=True, )

    shopify_transaction_ids = fields.One2many(
        string='Shopify Transaction',
        comodel_name='shopify.transactions',
        inverse_name='sale_id',
    )

    shopify_refund_ids = fields.One2many(
        string='Shopify Refunds',
        comodel_name='shopify.refunds',
        inverse_name='sale_id',
    )

    shopify_refund_transaction_ids = fields.One2many(
        string='Shopify Refunds Transaction',
        comodel_name='shopify.refunds.transaction',
        inverse_name='sale_id',
    )

    shopify_fulfilment_ids = fields.One2many(
        string='Shopify Fulfilment',
        comodel_name='shopify.fulfilment',
        inverse_name='sale_order_id',
    )

    shopify_is_invoice = fields.Boolean(string="Is shopify invoice paid?", default=False)

    shopify_is_refund = fields.Boolean(string="Is shopify credit note paid?", default=False)

    transaction_fee_tax_amount = fields.Monetary()

    transaction_fee_total_amount = fields.Monetary()

    refund_fee_tax_amount = fields.Monetary()

    refund_fee_total_amount = fields.Monetary()

    shopify_tag_ids = fields.Many2many('crm.tag', string="Shopify Tags")

    coupon_ids = fields.Many2many('shopify.coupon', string="Shopify Coupons")

    shopify_sale_channel = fields.Selection(string='Shopify Sale Channel', selection=[('pos', 'Point of Sale'),
                                                                                      ('web', 'Online Store'),
                                                                                      ('subscription_contract', 'Subscription Contract'),
                                                                                      ('shopify_draft_order',
                                                                                       'Draft Order'),
                                                                                      ('Matrixify App', 'Matrixify App')])

    shopify_err_tag_ids = fields.Many2many('shopify.err.tag', string='Shopify Error Tags')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    shopify_id = fields.Char(string="Shopify Id", readonly=True, store=True)

    line_coupon_ids = fields.Many2many('shopify.coupon', string="Shopify Coupons Line")
