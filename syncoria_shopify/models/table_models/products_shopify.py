# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import re
import datetime
from odoo.exceptions import AccessError, UserError
from ...shopify.utils import *
from odoo import models, api, fields, tools, exceptions, _

import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    shopify_product = fields.Boolean(string='Is Shopify Product', copy=False, default=False)

    shopify_image_id = fields.Char(
        string="Shopify Image Id", store=True, copy=False)

    shopify_inventory_id = fields.Char(
        string="Shopify Inventory Id", store=True, copy=False)

    shopify_categ_ids = fields.One2many('shopify.product.category',
                                        'product_tmpl_id',
                                        string="Shopify Categories")

    shopify_type = fields.Char(string="Shopify Product Type",
                               readonly=True, store=True)

    custom_option = fields.Boolean(string="Custom Option", default=False)

    shopify_published_scope = fields.Char()

    shopify_tags = fields.Char()

    shopify_template_suffix = fields.Char()

    shopify_variants = fields.Char()

    shopify_vendor = fields.Char()

    shopify_compare_price = fields.Monetary(string='Compare at price',
                                            help="To display a markdown, enter a value higher than your price")

    shopify_charge_tax = fields.Boolean(string='Charge tax?')

    shopify_product_status = fields.Selection(
        string='Product status',
        selection=[('draft', 'Draft'), ('active', 'Active'),
                   ('archived', 'Archived')],
        default='active',
    )

    shopify_collections = fields.Char()

    shopify_origin_country_id = fields.Many2one(
        string='Shopify Country Code of Origin',
        comodel_name='res.country',
        ondelete='restrict',
    )

    shopify_province_origin_id = fields.Many2one(
        string='Shopify Province Code of Origin',
        comodel_name='res.country.state',
        ondelete='restrict',
    )

    shopify_currency_id = fields.Many2one(
        string='Shopify Currency',
        comodel_name='res.currency',
        ondelete='restrict',
    )

    shopify_price = fields.Float()

    shopify_update_variants = fields.Boolean()

    shopify_show_on_hand_qty_status_button = fields.Boolean(
        compute='_shopify_compute_show_qty_status_button')

    shopify_show_forecasted_qty_status_button = fields.Boolean(
        compute='_shopify_compute_show_qty_status_button')

    def _shopify_compute_show_qty_status_button(self):
        for template in self:
            template.shopify_show_on_hand_qty_status_button = template.type == 'product'
            template.shopify_show_forecasted_qty_status_button = template.type == 'product'

    shopify_qty_available = fields.Float(
        'Shopify Qty On Hand', compute='_compute_shopify_quantities',
        compute_sudo=False, digits='Product Unit of Measure')

    def _compute_shopify_quantities(self):
        res = self._compute_shopify_quantities_dict()
        for template in self:
            template.shopify_qty_available = res[template.id]['shopify_qty_available']

class ProductProductShopify(models.Model):
    _inherit = 'product.product'

    shopify_categ_ids = fields.One2many('shopify.product.category',
                                        'product_id',
                                        string="Shopify Categories")

    shopify_type = fields.Char(readonly=True, store=True)

    shopify_com = fields.Char()

    shopify_image_id = fields.Char(string="Shopify Image Id", store=True, copy=False)

    shopify_origin_country_id = fields.Many2one(
        string='Shopify Country Code of Origin',
        comodel_name='res.country',
        related='product_tmpl_id.shopify_origin_country_id',
        readonly=True,
    )

    shopify_province_origin_id = fields.Many2one(
        string='Shopify Province Code of Origin',
        comodel_name='res.country.state',
        related='product_tmpl_id.shopify_province_origin_id',
        readonly=True,
    )

    shopify_currency_id = fields.Many2one(
        string='Shopify Currency',
        comodel_name='res.currency',
        related='product_tmpl_id.shopify_currency_id',
        readonly=True,
    )

    shopify_price = fields.Float(string='Shopify Product Price', )

    inventory_stock_updated = fields.Boolean()

    shopify_qty_available = fields.Float(
        'Shopify Qty On Hand', compute='_compute_shopify_quantities',
        digits='Product Unit of Measure', compute_sudo=False,
        help="Current quantity of products.\n"
             "In a context with a single Stock Location, this includes "
             "goods stored at this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods stored in the Stock Location of this Warehouse, or any "
             "of its children.\n"
             "stored in the Stock Location of the Warehouse of this Shop, "
             "or any of its children.\n"
             "Otherwise, this includes goods stored in any Stock Location "
             "with 'internal' type.")

    shopify_product_mapping_ids = fields.One2many('shopify.product.mappings', 'product_id', string='Instance Mappings')

    shopify_need_sync = fields.Boolean(string='Need to Sync To Shopify?')

    def _compute_shopify_quantities(self):
        products = self.filtered(lambda p: p.type != 'service')
        services = self - products
        products.shopify_qty_available = 0.0
        services.shopify_qty_available = 0.0
        instance_id = self.marketplace_instance_id
        if instance_id and instance_id.warehouse_id:
            warehouse_id = self.env['stock.warehouse'].browse(instance_id.warehouse_id.id)
            for product in products:
                product.shopify_qty_available = product.with_context({'warehouse': warehouse_id.id}).qty_available

    compare_at_price = fields.Char()

    fulfillment_service = fields.Char()

    inventory_management = fields.Char()

    inventory_policy = fields.Char()

    requires_shipping = fields.Boolean()

    taxable = fields.Boolean()

    shopify_vendor = fields.Char()

    shopify_collections = fields.Char()

    shopify_parent_id = fields.Char()


class ProductCategShopify(models.Model):
    _inherit = 'product.category'

    shopify_id = fields.Integer(string="Shopify ID", readonly=True, store=True)


class ShopifyCategory(models.Model):
    _name = 'shopify.product.category'

    _description = 'shopify Product Category'

    _rec_name = 'categ_name'

    name = fields.Many2one('product.category', string="Category")

    categ_name = fields.Char(string="Actual Name")

    product_tmpl_id = fields.Many2one('product.template', string="Product Template Id")

    product_id = fields.Many2one('product.product')


# class ProductAttributeExtended(models.Model):
#     _inherit = 'product.attribute'
#
#     attribute_set_id = fields.Integer(string="Ids")
#     # attribute_set = fields.Many2one('product.attribute.set')
#
# class SCPQ(models.TransientModel):
#     _inherit = 'stock.change.product.qty'
#
#


class ProductTemplateAttributeLine(models.Model):
    _inherit = 'product.template.attribute.line'

    shopify_value_ids = fields.Many2many('product.attribute.value',
                                         string="Shopify Exclude Values",
                                         domain="[('attribute_id', '=', attribute_id)]",
                                         relation='shopify_pav_ptal_rel',
                                         ondelete='restrict')

#     shopify_value_count = fields.Integer(compute='_compute_shopify_value_count', store=True, readonly=True)
#
#     @api.depends('shopify_value_ids')
#     def _compute_shopify_value_count(self):
#         for record in self:
#             record.shopify_value_count = len(record.shopify_value_ids)
#
#     web_excl_value_ids = fields.Many2many('product.attribute.value', string="Website Exclude Values", domain="[('attribute_id', '=', attribute_id)]",
#         relation='webexcl_pav_ptal_rel', ondelete='restrict')


# class ShopifyProductCollection(models.Model):
#     _name = 'shopify.product.collection'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _description = 'Shopify Product Collection'

#     _rec_name = 'title'
#     _order = 'title ASC'

#     title = fields.Char(
#         string='Title',
#         required=True,
#         default=lambda self: _('New'),
#         copy=False,
#         size=255,
#     )
#     body_html = fields.Text(copy=False)
#     handle = fields.Char(copy=False)
#     image_id = fields.Many2one(comodel_name='ir.attachment', ondelete='set null', copy=False)
#     shopify_id = fields.Char('Shopify ID', copy=False)#Big Integer
#     shopify_published = fields.Boolean('Published', copy=False)
#     shopify_published_at = fields.Datetime('Shopify Published At', copy=False)
#     shopify_published_scope = fields.Selection(
#         string='Published Scope',
#         selection=[('web', 'Web'), ('global', 'Global')],
#     )
#     shopify_sort_order = fields.Selection(
#         string='Sort Order',
#         selection=[
#             ('alpha-asc', 'Alphabetically, in ascending order (A - Z).'),
#             ('alpha-desc', 'Alphabetically, in descending order (Z - A).'),
#             ('best-selling', 'By best-selling products.'),
#             ('created', 'By date created, in ascending order (oldest - newest).'),
#             ('created-desc', 'By date created, in descending order (newest - oldest).'),
#             ('manual', 'Order created by the shop owner.'),
#             ('price-asc', 'By price, in ascending order (lowest - highest).'),
#             ('price-desc', 'By price, in descending order (highest - lowest).'),
#         ],
#     )
#     shopify_template_suffix = fields.Selection(
#         selection=[('custom', 'Custom'), ('null', 'Null')],
#         default='custom',
#     )
#     shopify_updated_at = fields.Datetime()
#     product_ids = fields.Many2many(
#         string='Products',
#         comodel_name='product.template',
#         relation='product_template_shopify_collection_rel',
#         column1='product_template_id',
#         column2='shopify_collection_id',
#         domain=[('shopify_id', '!=', False)],
#     )
#     instance_id = fields.Many2one(
#         string='Marketplace Instance',
#         comodel_name='marketplace.instance',
#         ondelete='restrict',
#     )
#     collection_image = fields.Image("Collection Image", max_width=128, max_height=128)

#     def get_collection_url(self):
#         host = self.instance_id.marketplace_host
#         api_version = self.instance_id.marketplace_api_version
#         collection_id = self.shopify_id
#         url = f'{host}/admin/api/{api_version}/custom_collections/{collection_id}.json'
#         if 'http' not in url:
#             url = 'https://' + url
#         return url

#     def get_collection_products_url(self):
#         host = self.instance_id.marketplace_host
#         api_version = self.instance_id.marketplace_api_version
#         collection_id = self.shopify_id
#         url = f'{host}/admin/api/{api_version}/collections/{collection_id}/products.json'
#         if 'http' not in url:
#             url = 'https://' + url
#         return url

#     def delete_shopify_collection_product(self, product_id):
#         headers = self.get_headers()
#         host = self.instance_id.marketplace_host
#         api_version = self.instance_id.marketplace_api_version
#         url = f'{host}/admin/api/{api_version}/collects/{product_id}.json'
#         url = 'https://' + url if 'http' not in url else url

#         data = requests.delete(url=url, headers=headers)

#         if data.status_code == 200:
#             _logger.info(f"Shopify Collection Product ID-{product_id} deleted successfully!")
#         else:
#             _logger.info(f"Shopify Collection Product ID-{product_id} deletion unsuccessful")

#     def add_shopify_collection_product(self, product_id):
#         headers = self.get_headers()
#         host = self.instance_id.marketplace_host
#         api_version = self.instance_id.marketplace_api_version
#         url = f'{host}/admin/api/{api_version}/collects.json'
#         url = 'https://' + url if 'http' not in url else url

#         collect_product_dict = {
#             'collect' : {
#                 'product_id' : product_id,
#                 'collection_id' : self.shopify_id,
#             }
#         }

#         data = requests.post(url=url, headers=headers, data=json.dumps(collect_product_dict))

#         if data.status_code == 201:
#             _logger.info(f"Shopify Collection Product ID-{product_id} added successfully!")
#         else:
#             _logger.info(f"Shopify Collection Product ID-{product_id} addition unsuccessful")


#     def convert_shopify_dt_to_odoo_dt(self, shopify_dt):
#         timeformat = shopify_dt.split('+')[-6:]
#         odoo_dt = shopify_dt[0:-6].replace('T',' ')
#         return odoo_dt

#     def get_headers(self):
#         headers = {}
#         headers['X-Shopify-Access-Token'] = self.instance_id.marketplace_api_password
#         headers['Content-Type'] = 'application/json'
#         return headers

#     def convert_odoo_collection_to_shopify_dictionary(self):
#         collection_dict = {}
#         collection_dict.update({
#             'custom_collection' : {
#                 'id' : self.shopify_id,
#                 'body_html' : self.body_html,
#             }
#         })
#         return collection_dict

#     def convert_shopify_collection_to_odoo_dictionary(self, collection_read):
#         collection_dict = {}

#         if collection_read.get('title'):
#             collection_dict['title'] = collection_read.get('title')
#         if collection_read.get('body_html'):
#             collection_dict['body_html'] = collection_read.get('body_html')
#         if collection_read.get('handle'):
#             collection_dict['handle'] = collection_read.get('handle')
#         if collection_read.get('id'):
#             collection_dict['shopify_id'] = collection_read.get('id')
#         if collection_read.get('published'):
#             collection_dict['shopify_published'] = collection_read.get('published')
#         if collection_read.get('published_at'):
#             collection_dict['shopify_published_at'] = self.convert_shopify_dt_to_odoo_dt(collection_read.get('published_at'))
#         if collection_read.get('published_scope'):
#             collection_dict['shopify_published_scope'] = collection_read.get('published_scope')
#         if collection_read.get('sort_order'):
#             collection_dict['shopify_sort_order'] = collection_read.get('sort_order')
#         if collection_read.get('template_suffix'):
#             collection_dict['shopify_template_suffix'] = collection_read.get('template_suffix')
#         if collection_read.get('updated_at'):
#             collection_dict['shopify_updated_at'] = self.convert_shopify_dt_to_odoo_dt(collection_read.get('updated_at'))

#         return collection_dict

#     def get_shopify_collection_data(self):
#         url = self.get_collection_url()
#         headers = self.get_headers()
#         data = requests.get(url=url, headers=headers)

#         if data.status_code == 200:
#             data = data.json()
#             return data

#         return False

#     def shopify_import_collection_data(self):
#         if self.instance_id and self.shopify_id:
#             collection_data = self.get_shopify_collection_data()

#             if collection_data.get('custom_collection'):

#                 collection_read = collection_data.get('custom_collection')
#                 collection_dict = self.convert_shopify_collection_to_odoo_dictionary(collection_read)

#                 if collection_dict:
#                     self.write(collection_dict)

#                     self.import_shopify_collection_products(self.instance_id, self.shopify_id)
#                     self.message_post(body=_(f"Collection Id- {self.shopify_id} successfully imported in Odoo."))

#             return False


#     def shopify_import_collection_products_data(self):
#         if self.instance_id and self.shopify_id:
#             url = self.get_collection_products_url()
#             headers = self.get_headers()
#             data = requests.get(url=url, headers=headers)

#             if data.status_code == 200:
#                 data = data.json()
#                 return data

#             return False


#     def shopify_import_collection(self):
#         collection_read = self.shopify_import_collection_data()
#         if collection_read:
#             self.import_shopify_collection_products(self.instance_id, self.shopify_id)
#         else:
#             print("No Collection data imported!")

#     def shopify_export_collection(self):
#         if self.instance_id and self.shopify_id:
#             try:
#                 url = self.get_collection_url()
#                 headers = self.get_headers()
#                 collection_dict = self.convert_odoo_collection_to_shopify_dictionary()
#                 data = requests.put(url=url, headers=headers, data=json.dumps(collection_dict))

#                 if data.status_code == 200:
#                     data = data.json()
#                     products_data = self.shopify_import_collection_products_data()

#                     shopify_product_ids = []
#                     shopify_product_ids_dict = {}
#                     if products_data:
#                         shopify_product_ids
#                         if products_data.get('products'):
#                             for product in products_data['products']:
#                                 if product.get('options'):
#                                     for option in product.get('options'):
#                                         shopify_product_ids += [str(option['product_id'])]
#                                         shopify_product_ids_dict[str(option['product_id'])] = str(product.get('id'))

#                         odoo_product_ids = self.product_ids.mapped('shopify_id')

#                         needs_to_add_products = list(set(odoo_product_ids) - set(shopify_product_ids))
#                         needs_to_delete_products  = list(set(shopify_product_ids) - set(odoo_product_ids))


#                         for product_id in needs_to_delete_products:
#                             product_id = shopify_product_ids_dict.get(product_id)
#                             self.delete_shopify_collection_product(product_id)

#                         for product_id in needs_to_add_products:
#                             self.add_shopify_collection_product(product_id)


#                     if data.get('custom_collection'):
#                         self.message_post(body=_("Collection updated successfully on Shopify"))
#                     else:
#                         raise UserError(_("No Custom Collections found in Shopify"))
#                 else:
#                     raise UserError(_("Error: {}".format(data.text)))

#             except Exception as e:
#                 raise UserError(_("Error: {}".format(e.args)))


#     def import_shopify_collection_products(self, instance_id, collection_id):
#         products_data = self.shopify_import_collection_products_data()

#         if products_data:
#             if products_data.get('products'):
#                 products = products_data.get('products') if type(
#                     products_data['products']) == list else [products_data['products']]

#                 _logger.info(f"Number of Collection Productions for Collection ID: {collection_id} - {len(products)}")

#                 products_ids = [product['id'] for product in products]

#                 for product_id in products_ids:    
#                     product_tmpl_id = self.env['product.template'].search([('shopify_id', '=', product_id)], limit=1)
#                     if product_tmpl_id:
#                         if str(product_id) not in self.product_ids.mapped('shopify_id'):
#                             self.product_ids = self.product_ids.ids + product_tmpl_id.ids


#             else:
#                 raise UserError(
#                     _("No Custom Collections found in Shopify"))


#     def process_shopify_collection_product(self, products_read, collection_id):
#         if products_read.get('id'):
#             product_template = self.env['product.template']

#             if str(products_read.get('id')) not in collection_id.product_ids.mapped('shopify_id'):
#                 product_tmpl_id = product_template.search([('shopify_id', '=', products_read.get('id'))], limit=1)

#                 if product_tmpl_id:
#                     collection_id.product_ids =  collection_id.product_ids.ids + product_tmpl_id.ids
#                     collection_id._cr.commit()


# class IrAttachment(models.Model):
#     _inherit = 'ir.attachment'

#     shopify_attachment = fields.Binary()
#     src = fields.Char()
#     alt = fields.Char()
#     shopify_created_at = fields.Datetime()
#     shopify_width = fields.Integer()
#     shopify_height = fields.Integer()
#     shopify_collection_id = fields.Many2one(comodel_name='shopify.product.collection',  ondelete='set null')
