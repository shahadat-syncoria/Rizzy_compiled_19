# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
import random
import time

from odoo import models, fields, api, _
from odoo.http import request
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
import logging
import pprint
import json
import pytz

from odoo.addons.odoosync_base.utils.app_payment import AppPayment

_logger = logging.getLogger(__name__)

def generate_idempotency_key():
    current_time_struct = time.localtime()
    timestamp_part = time.strftime("%Y%m%d%H%M%S", current_time_struct)
    random_part = random.randint(10, 99)
    idempotency_key = f"{timestamp_part}{random_part}"
    return idempotency_key


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    use_cloud_terminal = fields.Boolean(string="Use cloud terminal")

    support_mcloud_terminal = fields.Boolean()

    payment_type_inbound = fields.Boolean()

    payment_type_outbound = fields.Boolean()

    moneris_payment_status = fields.Selection(
        string='Payment Status',
        selection=[
            ('pending', 'Pending'),
            ('waiting', 'Waiting'),
            ('done', 'Done'),
            ('retry', 'Retry'),
            ('waitingCancel', 'Waiting Cancel'),
            ('reversing', 'Reversing'),
            ('reversed', 'Reversed'),
        ], default='pending'
    )

    moneris_move_name = fields.Char(compute='_onchange_journal_id')

    moneris_is_manual_payment = fields.Boolean(string="Is Manual Payment?", default=False)

    compute_domain_moneris_account_payment = fields.Binary(readonly=True,store=True)

    moneris_account_payment = fields.Many2one("account.payment",string="Moneris Account Payment" )

    moneris_refund_card_info = fields.Char(string="Moneris Payment Card info")

    moneris_refundable_amount = fields.Monetary(
        string="Moneris Refundable Amount",
        currency_field='currency_id',
        related='moneris_account_payment.moneris_refundable_amount',
        readonly=True,
    )

    moneris_device_id = fields.Many2one("moneris.device", ondelete='restrict',
        domain=lambda self: [('journal_id', '=', self.id)],)

    moneris_device_name = fields.Char(
        string='Moneris Device ID',
        related='moneris_device_id.code')

    moneris_cloud_receiptid = fields.Char(store=True)

    moneris_cloud_transid = fields.Char(store=True)
