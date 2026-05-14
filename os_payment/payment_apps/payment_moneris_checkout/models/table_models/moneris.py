# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
import re

from odoo import models, fields, api
from odoo.http import request
from odoo.exceptions import UserError
from odoo.service import common
from ...lib import mpgClasses
from datetime import datetime
import string
import random
import requests
import json
import pprint
import logging
import urllib.parse
from odoo.addons.odoosync_base.utils.app_payment import AppPayment

_logger = logging.getLogger(__name__)
version_info = common.exp_version()
server_serie = version_info.get('server_serie')

TRANSACTION_CODES = {
    "00": "PURCHASE",
    "01": "PRE-AUTHORIZATION",
    "06": "CARD-VERIFICATION",
}

ELECTRONIC_COMMERCE_INDICATOR = {
    "5": "Authenticated e-commerce transaction (3-D Secure)",
    "6": "Non-authenticated e-commerce transaction (3-D Secure)",
    "7": "SSL-enabled merchant",
}

RESULT = {
    "a": "Accepted",
    "d": "Declined",
}

CARD_TYPE = {
    "V": "Visa",
    "M": "Mastercard",
    "DC": "Diner's Card",
    "NO": "Novus/Discover",
    "D": "INTERAC® Debit",
    "C1": "JCB",
}

TRANSACTION_TYPES = [
    # ("preauthorization", "Preauthorization"),
    ("purchase", "Purchase"),
    ("cardverification", "Card Verification")
]

CVD_RESULT = {
    "1": "Success",
    "2": "Failed",
    "3": "Not performed",
    "4": "Card not eligible",
}

CONDITION = {
    "0": "Optional",
    "1": "Mandatory",
}

STATUS = [
    ("success", "Fraud tool successful"),
    ("failed", "Fraud tool failed (non-auto decision)"),
    ("disabled", "Fraud tool not performed"),
    ("ineligible", "Fraud tool was selected but card is not a credit card or card not eligibl"),
    ("failed_optional", "Fraud tool failed and auto decision is optional"),
    ("failed_mandatory", "Fraud tool failed auto decision is mandatory"),
]

DETAILS = [
    ("0", "Optional"),
    ("1", "Mandatory"),
]

FRAUD_TYPES = [
    ('cvd', 'CVD'),
    ('avs', 'AVS'),
    ('3d_secure', '3D Secure'),
    ('kount', 'Kount')
]

def remove_charandaccents(string):
    if string != None:
        return re.sub(r'[^ \nA-Za-z0-9/]+', '', string)
    else:
        return ''

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_url_id(href):
    url_id = False
    href = href.split("#")[1] if "#" in href else href.split("?")[1]
    vals = {}
    for item in href.split("&"):
        key, value = item.split("=")
        vals[key] = value
    return vals.get('id')


def url_to_dict(url_str):
    print(url_str)
    url_dict = urllib.parse.parse_qs(url_str)
    print("URL Params : " + str(url_dict))


def get_five_mins_ago(current_datetime):
    import datetime
    if isinstance(current_datetime, datetime.datetime):
        current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    five_mins_ago = datetime.datetime.strptime(
        current_datetime, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(minutes=5)
    return five_mins_ago.strftime('%Y-%m-%d %H:%M:%S')


def get_sale_lock(env):
    ICPSudo = env['ir.config_parameter'].sudo()
    sale_lock = ICPSudo.get_param('sale.group_auto_done_setting')
    return sale_lock


def get_href_params(request_object):
    # Extract the URL from the request object
    url = str(request_object).split()[1][1:-2]

    # Check if '?' exists in the URL
    url = url.split('?')[1] if '?' in url else url

    # Initialize an empty dictionary to store parameters
    href_params = {}

    # Split the URL by '&' to separate individual parameters
    for params in url.split('&'):
        # Split each parameter by '=' to get key and value
        key, value = params.split('=')

        # Add the key-value pair to the dictionary
        href_params[key] = value

    return href_params


class providerMoneris(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('monerischeckout', (
        'Moneris Checkout'))], ondelete={'monerischeckout': 'set default'})

    moneris_transaction_type = fields.Selection(
        string=('Moneris Transaction Type'),
        selection=TRANSACTION_TYPES,
        default='purchase',
        required=True)

    moneris_store_id = fields.Char(
        string='Store ID', help='Store Id in Moneris Direct Host Configuration')

    moneris_api_token = fields.Char(
        string='Api Token', help='Api Token in Moneris Direct Host Configuration')

    moneris_checkout_id = fields.Char()

    moneris_order_confirmation = fields.Selection(string='Moneris Order Confirmation', selection=[
        ('capture', ('Authorize & capture the amount and conform it'))], default='capture')

    moneris_store_card = fields.Selection(string='Store Card Data', selection=[
        ('never', 'Never'),
        ('customer', 'Let the customer decide'),
        ('always', 'Always')], default='never')

    moneris_avs = fields.Boolean(string='AVS', )

    moneris_avs_zip = fields.Boolean(string='Enable Zip', )

    moneris_cvv = fields.Boolean(string='CVV', default=True)

    moneris_3d_secure = fields.Boolean(string='3D Secure', )

    moneris_kount = fields.Boolean(string='Kount', )

    fees_active = fields.Boolean(default=False)

    fees_dom_fixed = fields.Float(default=0.35)

    fees_dom_var = fields.Float(default=3.4)

    fees_int_fixed = fields.Float(default=0.35)

    fees_int_var = fields.Float(default=3.9)

    allow_token_delete = fields.Boolean(
        string='Allow Token Delete',
        default=True,
        help='This field allows all users to delete other user `Payment Token`.'
    )

    moneris_token = fields.Boolean(string='Tokenization')

    moneris_lock_order = fields.Boolean(
        string='Lock Confirmed Sales',
        default=True,
    )

    moneris_recurring_invoice_scope = fields.Selection(
        selection=[
            ('overdue', 'Overdue invoices only'),
            ('all', 'All open invoices'),
        ],
        string='Recurring Invoice Scope',
        default='overdue',
        help='Select which invoices will be charged by the recurring payment scheduler.',
    )


class TxMoneris(models.Model):
    _inherit = 'payment.transaction'

    moneris_txn_type = fields.Char('Transaction type')

    moneris_customer_id = fields.Char('Customer Id')

    moneris_receipt_id = fields.Char('Receipt Id')

    moneris_response_code = fields.Char('Response Code')

    moneris_credit_card = fields.Char('Credit Card')

    moneris_card_name = fields.Char('Moneris Card Type')

    moneris_expiry_date = fields.Char('Expiry Date')

    moneris_transaction_time = fields.Char('Transaction Time')

    moneris_transaction_date = fields.Char('Transaction Date')

    moneris_transaction_id = fields.Char('Transaction ID')

    moneris_payment_type = fields.Char('Payment Type')

    moneris_reference_no = fields.Char('Reference Number')

    moneris_bank_approval = fields.Char('Bank Approval')

    moneris_card_holder = fields.Char('Cardholder')

    moneris_order_id = fields.Char('Response Order Id')

    moneris_iso_code = fields.Char('Iso Code')

    moneris_transaction_key = fields.Char('Transaction Key')

    moneris_transaction_no = fields.Char('Transaction Number')

    moneris_card_amount = fields.Char()

    moneris_cvd_result = fields.Char()

    moneris_avs_result = fields.Char()

    moneris_card_type = fields.Char(string='Moneris Payment Method')

    moneris_gift_txntype = fields.Char("Txn Type")

    moneris_gift_cardnum = fields.Char("Gift Card Num")

    moneris_gift_refnum = fields.Char("Gift Ref Num")

    moneris_gift_orderno = fields.Char("Gift Order No")

    moneris_gift_txnnum = fields.Char("Gift Txn Num")

    moneris_rem_balance = fields.Char("Remaining Balance")

    moneris_gift_display = fields.Char("Gift Display")

    moneris_card_description = fields.Char("Card Desecription")

    moneris_gift_charge = fields.Char("Gift Charge")

    moneris_voucher_text = fields.Char("Voucher Text")

    gift_lines = fields.One2many('transaction.gift.lines', 'gift_id')

    moneris_auth_code = fields.Char()

    moneris_bank_totals = fields.Char()

    moneris_complete = fields.Char()

    moneris_corporate_card = fields.Char()

    moneris_is_visa_debit = fields.Char()

    moneris_ticket = fields.Char()

    moneris_response = fields.Text()

    moneris_fraud_lines = fields.One2many(
        'moneris.fraud.lines', 'transaction_id')

    # def _monerischeckout_create_transaction_request(self, opaque_data):
    #     """ Create an Authorize.Net payment transaction request.

    #     Note: self.ensure_one()

    #     :param dict opaque_data: The payment details obfuscated by Authorize.Net
    #     :return:
    #     """
    #     self.ensure_one()

    #     authorize_API = AuthorizeAPI(self.provider_id)
    #     if self.provider_id.capture_manually or self.operation == 'validation':
    #         return authorize_API.authorize(self, opaque_data=opaque_data)
    #     else:
    #         return authorize_API.auth_and_capture(self, opaque_data=opaque_data)


class PaymentToken(models.Model):
    _inherit = 'payment.token'

    moneris_profile = fields.Char(
        string='Moneris Profile ID', help="Datakey in the Moneris Vault.")

    moneris_ticket = fields.Char(string='Moneris Ticket No')

    moneris_verified = fields.Boolean(string='Moneris Verified', )

    provider = fields.Selection(
        string='Provider', related='provider_id.code', readonly=False)

    save_token = fields.Boolean(
        string='Save Cards', related='provider_id.allow_tokenization', readonly=False)

    moneris_recurring = fields.Boolean(
        string='Recurring Payment',
        help='Enable this token for automated recurring invoice payments.',
    )

    # def unlink(self):
    #     if self.provider_id.code == 'monerischeckout':
    #         if not self.provider_id.allow_token_delete:
    #             print("user_partner_id===>>>" +
    #                   str(self.env.user.partner_id.id))
    #             print("partner_id===>>>" + str(self.partner_id.id))
    #             if self.env.user.partner_id.id != self.partner_id.id:
    #                 raise UserError(
    #                     _("You have no permission to delete this record. Only `%s` can delete his/her record." % (
    #                         self.partner_id.name)))
    #
    #     result = super(PaymentToken, self).unlink()
    #
    #     return result


class TransactionGiftLines(models.Model):
    _name = 'transaction.gift.lines'

    _description = 'Transaction Gift Lines'

    balance_remaining = fields.Char("Balance Remaining")

    first6last4 = fields.Char("f6l4")

    order_no = fields.Char("Order No.")

    reference_no = fields.Char("Refrence No")

    response_code = fields.Char("Response Code")

    transaction_amount = fields.Char("Transaction Amount")

    transaction_no = fields.Char("Transaction No.")

    gift_id = fields.Many2one('payment.transaction', string='Gift Id')


class MonerisFraudLines(models.Model):
    _name = 'moneris.fraud.lines'

    _description = 'Moneris Fraud Lines'

    transaction_type = fields.Selection(selection=FRAUD_TYPES, required=True)

    decision_origin = fields.Char("Decision Origin")

    result = fields.Char("Result")

    condition = fields.Char("Condition")

    status = fields.Char("Status")

    code = fields.Char("Code")

    details = fields.Char("Details")

    details_veres = fields.Char("VERes")

    details_pares = fields.Char("PARes")

    details_message = fields.Char("Message")

    details_cavv = fields.Char("CAVV")

    details_loadvbv = fields.Char("loadvbv")

    details_responsecode = fields.Char("Response Code")

    details_receipt_id = fields.Char("Receipt ID")

    details_score = fields.Char("Kount Score")

    details_error = fields.Char("Error")

    transaction_id = fields.Many2one(
        'payment.transaction', string='Transaction Id')
