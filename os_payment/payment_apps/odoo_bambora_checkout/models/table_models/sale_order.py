# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    payment_transaction_count = fields.Integer(
        string="Number of payment transactions",
        compute='_compute_payment_transaction_count')

    def _compute_payment_transaction_count(self):
        for rec in self:
            transaction_data = self.env['payment.transaction'].sudo().search(
                [('sale_order_ids', 'in', self.id)])
            rec.payment_transaction_count = len(transaction_data)
