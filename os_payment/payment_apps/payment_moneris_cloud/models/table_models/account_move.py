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

    moneris_request_id = fields.Char()

    moneris_last_action = fields.Char()

    moneris_transaction_id = fields.Char()

    moneris_idempotency_key = fields.Char()

    has_payments = fields.Boolean(
        compute="_compute_os_moneris_cloud_reconciled_payment_ids", help="Technical field used for usability purposes")

    reconciled_payments_count = fields.Integer(
        compute="_compute_os_moneris_cloud_reconciled_payment_ids")

    @api.depends('state')
    def _compute_os_moneris_cloud_reconciled_payment_ids(self):
        for record in self:
            record.reconciled_payments_count = 0
            if record.move_type == 'out_invoice' and record.name != '/' and record.state != 'draft':
                domain = [('ref', 'like', record.name),
                            ('payment_method_id.code', '=', 'electronic'),
                            ('payment_type', '=', 'outbound') ]


                AccPayment = self.env['account.payment']
                payments = AccPayment.search(domain)
                record.has_payments = bool(payments.ids)
                record.reconciled_payments_count = len(payments)


    # def action_post(self):
    #     if self.move_type == 'out_refund':
    #         split_name = "Reversal of: "
    #         if self.env.user.lang in ['fr_FR', 'fr_BE' , 'fr_CA', 'fr_CH']:
    #             split_name = 'Extourne de : '
    #         print(self.display_name)
    #         inv_name = self.display_name
    #         inv_name = inv_name.split(split_name)[1].split(",")[0]
    #         invoice = self.env['account.move'].sudo().search([('name','=',inv_name)])
    #         inv_amt = invoice.amount_residual
    #         domain = [('ref', 'like', inv_name),
    #                     ('payment_method_id.code', '=', 'electronic'),
    #                     ('payment_type', '=', 'outbound') ,
    #                     ('state','=','posted')]
    #         AccPayment = self.env['account.payment']
    #         refunds = AccPayment.search(domain)
    #
    #         if len(refunds) > 0 :
    #             refunds_sum = sum(refunds.mapped('amount'))
    #             print("\n self.amount-->", self.amount_residual,
    #                 "\n invoice.amount-->",  invoice.amount_total,
    #                 "\n refunds_sum-->", refunds_sum)
    #             if self.amount_residual >  invoice.amount_total - refunds_sum:
    #                 raise UserError(_('You can not refund with this amount'))
    #
    #     super(AccountMove, self).action_post()
