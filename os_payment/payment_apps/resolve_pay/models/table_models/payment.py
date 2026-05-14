# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import base64
import json

import logging
from odoo import models, fields, api, _,SUPERUSER_ID
_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('resolve', 'Resolve Pay')], ondelete={'resolve': 'set default'})


class AccountPayment(models.Model):
    _inherit = "account.payment"

    resolvepay_payment_date = fields.Char("Resolve Pay payment datetime")

    rp_payout_transaction_id = fields.Char("Resolve Pay Payout Transaction Id")

    rp_payout_id = fields.Char("Resolve Pay Payout Id")

    rp_payout_transaction_type = fields.Selection(selection=[('advance', 'advance'),
                                                             ('payment', 'payment'),
                                                             ('refund', 'refund'),
                                                             ('monthly_fee', 'monthly_fee'), ('annual_fee', 'annual_fee'),
                                                             ('non_advanced_invoice_fee', 'non_advanced_invoice_fee'),
                                                             ('merchant_payment', 'merchant_payment'),
                                                             ('mdr_extension', 'mdr_extension'),
                                                             ('credit_note', 'credit_note')], string='Resolve Pay Transaction Type')

    rp_payout_transaction_amount_gross = fields.Float('amount_gross')

    rp_payout_transaction_amount_fee = fields.Float('amount_fee')

    rp_payout_transaction_amount_net = fields.Float('amount_net')
