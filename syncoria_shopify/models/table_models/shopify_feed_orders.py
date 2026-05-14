# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import json
import requests
import base64
import re
from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timezone
import logging
_logger = logging.getLogger(__name__)


def get_address_vals(env, address):
    """Build res.partner child-address values from Shopify address payload."""
    address = address or {}
    country = False
    state = False

    country_domain = []
    if address.get("country_code"):
        country_domain += [("code", "=", address.get("country_code"))]
    elif address.get("country"):
        country_domain += [("name", "=", address.get("country"))]
    if country_domain:
        country = env["res.country"].sudo().search(country_domain, limit=1)

    state_domain = [("country_id", "=", country.id)] if country else []
    if address.get("province_code"):
        state_domain += [("code", "=", address.get("province_code"))]
    elif address.get("province"):
        state_domain += [("name", "=", address.get("province"))]
    if state_domain:
        state = env["res.country.state"].sudo().search(state_domain, limit=1)

    return {
        "name": address.get("name") or (
            ((address.get("first_name") or address.get("firstName") or "") + " " +
             (address.get("last_name") or address.get("lastName") or "")).strip()
        ),
        "street": address.get("address1") or "",
        "street2": address.get("address2") or "",
        "city": address.get("city") or "",
        "zip": address.get("zip") or "",
        "phone": address.get("phone") or "",
        "company_name": address.get("company") or "",
        "country_id": country.id if country else None,
        "state_id": state.id if state else None,
        "shopify_add_id": address.get("id"),
        "group_rfq": False,
        "group_on": False,
    }


class ShopifyFeedOrders(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _name = 'shopify.feed.orders'

    _description = 'Shopify Feed Orders'

    _rec_name = 'name'

    _order = 'name DESC'

    name = fields.Char(
        string='Name',
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('shopify.feed.orders'))

    instance_id = fields.Many2one(
        string='Marketplace Instance',
        comodel_name='marketplace.instance',
        ondelete='restrict',
    )

    shopify_id = fields.Char(string='Shopify Id', readonly=True)

    order_data = fields.Text(readonly=True)

    state = fields.Selection(
        string='State',
        tracking=True,
        selection=[('draft', 'Draft'), 
                   ('queue', 'Queue'),
                   ('processed', 'Processed'), 
                   ('failed', 'Failed')]
    )

    shopify_webhook_call = fields.Boolean(string='Webhook Call', readonly=True)

    shopify_app_id = fields.Char(string='App Id', readonly=True)

    shopify_confirmed = fields.Char(string='Confirmed', readonly=True)

    shopify_contact_email = fields.Char(string='Contact Email', readonly=True)

    shopify_currency = fields.Char(string='Currency', readonly=True)

    shopify_customer_name = fields.Char(string='Customer Name', readonly=True)

    shopify_customer_id = fields.Char(string='Customer ID', readonly=True)

    shopify_gateway = fields.Char(string='Gateway', readonly=True)

    shopify_order_number = fields.Char(string='Order Number', readonly=True)

    shopify_financial_status = fields.Char(string='Financial Status', readonly=True)

    shopify_fulfillment_status = fields.Char(string='Fulfillment Status', readonly=True)

    shopify_line_items = fields.Char(string='Line Items', readonly=True)

    shopify_user_id = fields.Char(string='User ID', readonly=True)

    sale_id = fields.Many2one(
        string='Odoo Order',
        comodel_name='sale.order',
        ondelete='set null',
    )

    """ ORDER SYNC """
