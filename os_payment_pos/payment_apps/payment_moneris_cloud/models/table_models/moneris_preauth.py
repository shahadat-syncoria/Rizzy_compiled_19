import logging

from odoo import fields, models, api
from odoo.addons.odoosync_base.utils.app_payment import AppPayment
import random
import string
import json
import time
from datetime import datetime
_logger = logging.getLogger(__name__)


class MonerisPreauth(models.Model):
    _name = "moneris.pos.preauth"

    _inherit = ["portal.mixin", "pos.bus.mixin", "pos.load.mixin", "mail.thread"]

    _description = "Point of Sale Preauth"

    _order = "order_date desc, name desc, id desc"

    name = fields.Char('Preauth Name')

    order_date = fields.Datetime('Order Date')

    order_id = fields.Char(string="Order ID")

    terminal_id = fields.Char(string="Terminal ID")

    total_amount = fields.Float(string="Total Amount")

    transaction_id = fields.Char(string="Transaction ID")

    status = fields.Selection([('pending', 'Pending'),
                               ('confirmed', 'Confirmed'),
                               ('failed', 'Failed'),('voided', 'Voided'),
                               ('settled','Settled')])

    customer_id = fields.Many2one('res.partner', string="Customer")

    moneris_go_payment_method = fields.Many2one('pos.payment.method', string="Payment Method")

    moneris_settled_order_id = fields.Many2one('pos.order', string="Settled Order")
