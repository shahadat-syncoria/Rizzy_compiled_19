# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import json
import requests
import base64
import re
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class ShopifyFeedCustomers(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _name = 'shopify.feed.customers'

    _description = 'Shopify Feed Customers'

    _rec_name = 'name'

    _order = 'name DESC'

    name = fields.Char(
        string='Name',
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('shopify.feed.customers'))

    instance_id = fields.Many2one(
        string='Marketplace Instance',
        comodel_name='marketplace.instance',
        ondelete='restrict',
    )

    shopify_id = fields.Char(string='Shopify Id', readonly=True)

    customer_data = fields.Text(
        string='Customer Data',
    )

    state = fields.Selection(
        string='state',
        tracking=True,
        selection=[('draft', 'draft'), ('queue', 'Queue'),
                   ('processed', 'Processed'), ('failed', 'Failed')]
    )

    customer_name = fields.Char()

    email = fields.Char()

    country_name = fields.Char()

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        ondelete='restrict',
    )
        # res_partner = self.env['res.partner'].sudo()
        # res_country = self.env['res.country'].sudo()
        # res_country_state = self.env['res.country.state'].sudo()

        # customer_dict = {}
        # customer_dict['shopify_id'] = customer['id']
        # if customer.get('name'):
        #     customer_dict['name'] = customer.get('name')
        # else:
        #     customer_dict['name'] = customer.get('first_name', '') + ' ' + customer.get('last_name', '') 

        # if customer.get('company'):
        #     company_id = res_partner.search([('is_company', '=', True), ('name', '=', customer.get('company'))], limit=1)
        #     if not company_id:
        #         company_id = res_partner.create({
        #             'name' : customer.get('company')
        #         })
        #     if company_id:
        #         customer_dict['parent_id'] = company_id.id

        # customer_dict['active'] = True
        # customer_dict['marketplace'] = True
        # customer_dict['marketplace_type'] = 'shopify'
        # customer_dict['shopify_instance_id'] = self.instance_id.id
        # customer_dict['email'] = customer.get('email', '')
        # customer_dict['phone'] = customer.get('phone', '')
        # customer_dict['type'] = 'contact'


        # child_ids = []
        # invoice_data_dict = {}
        # city = ''

        # default_address = customer.get('default_address')
        # if customer.get('addresses'):
        #     addresses = customer.get('addresses')
        #     if len(addresses) > 0 and customer.get('default_address'):
        #         for address in addresses:
        #             if address['id'] == default_address['id']:
        #                 customer_dict['city'] = address.get('city', '')
        #                 if address.get('country_code'):
        #                     country = res_country.search(
        #                         [('code', '=', address['country_code'])])
        #                     if country:
        #                         customer_dict['country_id'] = country.id
                        
        #                 if address.get('province_code'):
        #                     state = res_country_state.search(
        #                         [('code', '=', address['province_code'])])
        #                     customer_dict['state_id'] = state.id

        #                 customer_dict['phone'] = address.get('phone', '')
        #                 customer_dict['zip'] = address.get('zip', '')
        #                 customer_dict['street'] = address.get('address1', '')
        #                 customer_dict['street2'] = address.get('address2', '')
        #                 if address.get('company'):
        #                     company_id = res_partner.search([('is_company', '=', True), ('name', '=', address.get('company'))], limit=1)
        #                     if not company_id:
        #                         company_id = res_partner.create({
        #                             'name' : address.get('company')
        #                         })
        #                     if company_id:
        #                         customer_dict['parent_id'] = company_id.id


        # # if child_ids:
        # #     customer_dict['child_ids'] = child_ids
        # # New Fields
        # customer_dict['shopify_accepts_marketing'] = customer.get(
        #     'shopify_accepts_marketing')
        # customer_dict['shopify_last_order_id'] = customer.get('last_order_id')
        # customer_dict['shopify_last_order_name'] = customer.get('last_order_name')
        # customer_dict['marketing_opt_in_level'] = customer.get('marketing_opt_in_level')
        # customer_dict['multipass_identifier'] = customer.get('multipass_identifier')
        # customer_dict['orders_count'] = customer.get('orders_count')
        # customer_dict['shopify_state'] = customer.get('state')
        # customer_dict['comment'] = customer.get('note')
        # customer_dict['shopify_tax_exempt'] = customer.get('tax_exempt')
        # exempt_ids = []
        # if customer.get('tax_exempt'):
        #     for exempt in customer.get('tax_exemptions'):
        #         SpTaxExempt = self.env['shopify.tax.exempt']
        #         exempt_id = SpTaxExempt.sudo().search(
        #             [('name', '=', exempt)], limit=1)
        #         exempt_ids.append(exempt_id.id) if exempt_id else None
        # # customer_dict['shopify_tax_exemptions_ids'] = exempt_ids
        # customer_dict['shopify_total_spent'] = customer.get('total_spent')
        # customer_dict['shopify_verified_email'] = customer.get('verified_email')
        # # Property Payment Method Id
        # # instance_id = get_instance_id(self)
        # # customer_dict['property_payment_method_id'] = instance_id.marketplace_inbound_method_id.id
        # return customer_dict
