# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################


from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging


class AccountMove(models.Model):
    _inherit = 'account.move'

    has_payments = fields.Boolean(
        compute="_compute_os_clover_reconciled_payment_ids",
        help="Technical field used for usability purposes")

    reconciled_payments_count = fields.Integer(
        compute="_compute_os_clover_reconciled_payment_ids")

    clover_last_action = fields.Char()

    clover_last_response = fields.Text()

    @api.depends('state')
    def _compute_os_clover_reconciled_payment_ids(self):
        for record in self:
            record.reconciled_payments_count = 0
            if record.move_type == 'out_invoice' and record.name != '/' and record.state != 'draft':
                domain = [('ref', 'like', record.name),
                            ('payment_method_line_id.code', '=', 'electronic'),
                            ('payment_type', '=', 'outbound') ]


                AccPayment = self.env['account.payment']
                payments = AccPayment.search(domain)
                record.has_payments = bool(payments.ids)
                record.reconciled_payments_count = len(payments)
