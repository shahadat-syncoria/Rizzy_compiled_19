from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError


class ShopifyWarehouse(models.Model):
    _name = 'shopify.warehouse'

    _description = 'Shopify Warehouse'

    _rec_name = 'shopify_loc_name'

    shopify_invent_id = fields.Char("Inventory Id", )

    shopify_loc_name = fields.Char('Location Name')

    marketplace_type = fields.Selection(selection=[('shopify', 'Shopify')], default='shopify')

    shopify_instance_id = fields.Many2one("marketplace.instance", string="Shopify Instance ID")

    shopify_loc_add_one = fields.Char(string="Location Address1", )

    shopify_loc_add_two = fields.Char(string="Location Address2", )

    shopify_loc_city = fields.Char(string="Location City", )

    shopify_loc_zip = fields.Char(string="Location Zip", )

    shopify_loc_province = fields.Char(string="Location Province", )

    shopify_loc_country = fields.Char(string="Location Country", )

    shopify_loc_phone = fields.Char(string="Location Phone Number", )

    shopify_loc_created_at = fields.Char(string="Location Created", )

    shopify_loc_updated_at = fields.Char(string="Location Updated", )

    shopify_loc_country_code = fields.Char(string="Location Country Code", )

    shopify_loc_country_name = fields.Char(string="Location Country Name", )

    shopify_loc_country_province_code = fields.Char(string="Location Province Code", )

    shopify_loc_legacy = fields.Boolean(string="Location Leagacy", help="Can this location fulfil order?")

    shopify_loc_active = fields.Boolean(string="Active", )

    shopify_loc_localized_country_name = fields.Char(string="Localized Country Name", )

    shopify_loc_localized_province_name = fields.Char(string="Localized Province Name", )

    partner_id = fields.Many2one('res.partner',readonly=True,store=True)
