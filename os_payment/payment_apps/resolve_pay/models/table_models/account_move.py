import base64

from odoo import models, fields, api, _
import requests
from odoo.exceptions import UserError, ValidationError
import json, time
from datetime import date
import logging
_logger = logging.getLogger(__name__)


class Invoice(models.Model):
    _inherit = 'account.move'

    resolvepay_id = fields.Char(string='ResolvePay Invoice ID', tracking=True, copy=False)

    resolvepay_source = fields.Char(string='ResolvePay Source')

    resolvepay_customer_id = fields.Char(string='ResolvePay Customer ID', help='ID of the customer being charged.')

    resolvepay_order_number = fields.Char(string='Order Number', help='Order number identifier.')

    resolvepay_number = fields.Char(string='Invoice Number', help='Invoice number identifier.')

    resolvepay_po_number = fields.Char(string='PO Number', help='PO number identifier.')

    resolvepay_notes = fields.Char(string='Notes', help='Additional notes for the Customer')

    resolvepay_line_items = fields.Char(string='Line items', help='Line item data')

    resolvepay_merchant_invoice_url = fields.Char(string='Merchant invoice URL', help='The invoice PDF that you have uploaded to Resolve.')

    resolvepay_resolve_invoice_url = fields.Char(string='Resolve invoice URL', help='Resolve-issued invoice PDF with your invoice attached.')

    resolvepay_resolve_invoice_status = fields.Char(string='Invoice status', help='Shows current status of the Resolve-issued invoice PDF.')

    resolvepay_fully_paid_at = fields.Char(string='Fully paid at', help='The date the invoice has been fully paid.')

    resolvepay_advanced = fields.Boolean(string='Advanced', help='Indicates whether the invoice has been advanced.')

    resolvepay_due_at = fields.Char(string='Due at', help='The current due date for this invoice payment.')

    resolvepay_original_due_at = fields.Char(string='Original due at', help='The due date for this invoice at the time an advance was issued.')

    resolvepay_invoiced_at = fields.Char(string='Invoiced at', help='The date this invoice was created in your system of record (Resolve or Quickbooks).')

    resolvepay_advance_requested = fields.Boolean(string='Advance requested', help='Indicated if advance was requested.')

    resolvepay_terms = fields.Char(string='Terms', help='The terms selected for this invoice.')

    resolvepay_amount_payout_due = fields.Float(string='Amount payout due', help='The original amount that Resolve owed on this invoice on the advance date.')

    resolvepay_amount_payout_paid = fields.Float(string='Amount payout paid', help='The amount that Resolve has paid out.')

    resolvepay_amount_payout_pending = fields.Float(string='Amount payout pending', help='The amount that Resolve has currently pending to be paid out.')

    resolvepay_amount_payout_refunded = fields.Float(string='Amount payout refunded', help='The amount that Resolve has debited from due to refunds.')

    resolvepay_amount_payout_balance = fields.Float(string='Amount payout balance', help='The amount remaining to be paid out.')

    resolvepay_payout_fully_paid = fields.Float(string='Payout fully paid', help='The status of whether or not this invoice has been fully paid out.')

    resolvepay_payout_fully_paid_at = fields.Char(string='Payout fully paid at', help='The date of when this invoice has been fully paid out.')

    resolvepay_amount_balance = fields.Float(string='Amount balance', help='Current balance due.')

    resolvepay_amount_due = fields.Float(string='Amount due', help='Original amount due')

    resolvepay_amount_refunded = fields.Float(string='Amount refunded', help='Amount that has been refunded.')

    resolvepay_amount_pending = fields.Float(string='Amount pending', help='Amount of total payments pending.')

    resolvepay_amount_paid = fields.Float(string='Amount paid', help='Amount of total payments applied to this invoice.')

    resolvepay_amount_advance = fields.Float(string='Amount advance', help='Amount of advance received.')

    resolvepay_amount_advance_fee = fields.Float(string='Amount advance fee', help='Fee for the amount of advance.')

    resolvepay_amount_advance_fee_refund = fields.Float(string='Amount advance fee refund', help='Refunded fees for the amount of advance.')

    resolvepay_advance_rate = fields.Float(string='Advance rate', help='The advance rate that was used to determine amount of advance')

    resolvepay_advanced_at = fields.Char(string='Advanced at', help='The date this invoice was advanced.')

    resolvepay_amount_customer_fee_total = fields.Float(string='Amount customer fee total', help='The total amount of customer fees accrued.')

    resolvepay_amount_customer_fee_waived = fields.Float(string='Amount customer fee waived', help='The total amount of customer fees waived.')

    resolvepay_amount_customer_fee_paid = fields.Float(string='Amount customer fee paid', help='The total amount of customer fees paid.')

    resolvepay_amount_customer_fee_balance = fields.Float(string='Amount customer fee balance', help='The current amount of customer fees owed.')

    resolvepay_created_at = fields.Char(string='Created at', help='Date the customer was created.')

    resolvepay_updated_at = fields.Char(string='Updated at', help='Date the customer was last updated.')

    resolvepay_archived = fields.Char(string='Archived', help='Boolean indicating if invoice is archived.')

    resolvepay_charge_id = fields.Char(string='ResolvePay Charge Id')

    resolvepay_amount_available = fields.Float(string='Available Credit', related='partner_id.resolvepay_amount_available')

    payout_transaction_ids = fields.One2many(comodel_name='resolvepay.payout.transaction', inverse_name='move_id', string='Payout Transaction')
