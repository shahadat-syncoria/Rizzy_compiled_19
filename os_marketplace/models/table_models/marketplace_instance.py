# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.http import request

class MarketplaceInstance(models.Model):
    _inherit = ['mail.thread','mail.activity.mixin',]

    _name = 'marketplace.instance'

    _description = 'Marketplace Instance'

    _order = "id desc"

    token = fields.Char(string='Token', copy=False)

    account_id = fields.Many2one(
        string='Account',
        comodel_name='omni.account',
        ondelete='restrict',
    )

    marketplace_instance_type = fields.Selection(
        string='Instance Type',
        selection=[],
    )

    name = fields.Char(string='Instance Name', required=True,
                       copy=False, index=True, default=lambda self: _('New'))

    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        ondelete='restrict',
        required=True
    )

    marketplace_state = fields.Selection([
        ('draft', 'Not Confirmed'), 
        ('confirm', 'Confirmed')], 
        default='draft', string='State')

    warehouse_id = fields.Many2one(
        string='Warehouse',
        comodel_name='stock.warehouse',
        ondelete='restrict',
    )

    language_id = fields.Many2one(
        string='Language',
        comodel_name='res.lang',
        ondelete='restrict',
    )

    fiscal_position_id = fields.Many2one(
        string='Fiscal Position',
        comodel_name='account.fiscal.position',
        ondelete='restrict',
    )

    user_id = fields.Many2one(
        string='Salesperson',
        comodel_name='res.users',
        ondelete='restrict',
    )

    set_price = fields.Boolean(
        string='Set Price ?',
    )

    set_stock = fields.Boolean(
        string='Set Stock?',
    )

    set_image = fields.Boolean(
        string='Set Image?',
    )

    update_image_per_color = fields.Boolean(
        string='Update Image per Color?',
    )

    sync_product_image = fields.Boolean(
        string='Sync Images?', 
        default=True,
    )

    sync_price = fields.Boolean(
        string='Import/Sync Price?',
        default=True,
    )

    sync_qty = fields.Boolean(
        string='Sync Quantity?',
        default=True,
    )

    import_price = fields.Boolean(
        string='Import Price?',
        default=True,
    )

    import_product_image = fields.Boolean(
        string='Import Product Image?',
        default=True,
    )

    import_qty = fields.Boolean(
        string='Import Product Quantity?',
        default=True,
    )

    calculate_discount = fields.Boolean(
        string='Calculate Discount',
    )

    default_invoice_policy = fields.Selection(
        string='Invoicing Policy',
        selection=[('order', 'Ordered Quantities'),
                   ('delivery', 'Delivered Quantities')],
        default='order',
    )

    duplicate_barcode_check = fields.Boolean()

    pricelist_id = fields.Many2one(
        string='Pricelist',
        comodel_name='product.pricelist',
        ondelete='restrict',
    )

    payment_term_id = fields.Many2one(
        string='Payment Terms',
        comodel_name='account.payment.term',
        ondelete='restrict',
    )

    marketplace_journal_id = fields.Many2one(
        string='Refund Account Journal',
        comodel_name='account.journal',
        ondelete='restrict',
    )

    ao_import = fields.Boolean(string='Auto Order Import?')

    ao_import_interval = fields.Integer(default=1, help="Repeat every x.")

    ao_import_interval_type = fields.Selection([('minutes', 'Minutes'),
                                      ('hours', 'Hours'),
                                      ('days', 'Days'),
                                      ('weeks', 'Weeks'),
                                      ('months', 'Months')], string='Interval Type', default='hours')

    ao_import_nextcall = fields.Datetime(
        string='Next Import Execution Date', 
        default=fields.Datetime.now, 
        help="Next planned execution date for this job.")

    ao_import_user_id = fields.Many2one('res.users', 
        string='Scheduler User', 
        default=lambda self: self.env.user)

    ao_update = fields.Boolean(string='Auto Order Update?')

    ao_update_interval = fields.Integer(default=1, help="Repeat every x.")

    ao_update_interval_type = fields.Selection([('minutes', 'Minutes'),
                                      ('hours', 'Hours'),
                                      ('days', 'Days'),
                                      ('weeks', 'Weeks'),
                                      ('months', 'Months')], string='Interval Unit', default='hours')

    ao_update_nextcall = fields.Datetime(
        string='Next Execution Date', default=fields.Datetime.now, help="Next planned execution date for this job.")

    ao_update_user_id = fields.Many2one(
        'res.users', string='User', 
        default=lambda self: self.env.user)

    order_tracking_ref = fields.Boolean(
        string='One order can have multiple Tracking Number?',
    )

    order_prefix = fields.Char()

    auto_close_order = fields.Boolean(
        string='Auto Closed Order',
    )

    auto_create_product = fields.Boolean(
        string='Auto Create Product if not found?',
    )

    notify_customer = fields.Boolean(
        string='Notify Customer about Update Order Status',
    )

    sales_team_id = fields.Many2one(
        string='Sales Team',
        comodel_name='crm.team',
        ondelete='restrict',
    )

    auto_create_invoice = fields.Boolean(
        string='Auto Create Invoice?',
        default=True,
    )

    auto_create_fulfilment = fields.Boolean(
        string='Auto Create Fulfilment?',
        default=True,
    )

    analytic_account_id = fields.Many2one(
        string='Analytic Account',
        comodel_name='account.analytic.account',
        ondelete='restrict',
    )

    stock_auto_export = fields.Boolean(
        string='Stock Auto Export?',
    )

    stock_fields = fields.Selection(
        string='Stock Field',
        selection=[('onhand', 'Quantity on Hand (product.product)'),
                   ('Forecast', 'Forecast Quantity (product.product)')]
    )
