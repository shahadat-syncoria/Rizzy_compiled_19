# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
import time

from odoo import models, fields, api, exceptions, _
import logging
from odoo.exceptions import UserError
import os
import datetime
import base64
import requests
from fpdf import FPDF
from odoo.addons.odoosync_base.utils.app_payment import AppPayment

_logger = logging.getLogger(__name__)


class PosOrderPaymentInherit(models.Model):
    _inherit = 'pos.payment'

    is_moneris_cloud = fields.Boolean(string='Is Moneris Cloud', default=False)

    cloud_request_id = fields.Char("Cloud Request ID")

    purchase_cloud_ticket = fields.Char()

    payment_acquirer_name = fields.Char()

    purchase_receipt_id = fields.Char()

    cloud_receipt_customer = fields.Text("Customer Receipt")

    cloud_receipt_merchant = fields.Text("Merchant Receipt")

    cloud_val_responsecode = fields.Char("Validation Response Code")

    cloud_val_message = fields.Char("Validation Message")

    cloud_val_completed = fields.Char("Validation Completed")

    cloud_val_error = fields.Char("Validation Error")

    cloud_val_timeout = fields.Char("Validation Timeout")

    cloud_val_postbackurl = fields.Char("Validation Postback Url")

    cloud_val_cloudticket = fields.Char("Validation Cloud Ticket")

    moneris_cloud_completed = fields.Boolean("Completed")

    moneris_cloud_transtype = fields.Char("Trans Type")

    moneris_cloud_error = fields.Boolean("Error")

    moneris_cloud_initrequired = fields.Boolean("Init Required")

    moneris_cloud_safindicator = fields.Char("Saf Indicator")

    moneris_cloud_responsecode = fields.Char("Response Code")

    moneris_cloud_iso = fields.Char("ISO")

    moneris_cloud_languagecode = fields.Char("Language Code")

    moneris_cloud_partailauthamount = fields.Char("Partial Auth Amount")

    moneris_cloud_availablebalance = fields.Char("Available Balance")

    moneris_cloud_tipamount = fields.Char("TipAmount")

    moneris_cloud_emvcashbackamount = fields.Char("EMV Cash Back Amount")

    moneris_cloud_surchargeamount = fields.Char("Surcharge Amount")

    moneris_cloud_foreigncurrencyamount = fields.Char(
        "Foreign Currency Amount")

    moneris_cloud_baserate = fields.Char("Base Rate")

    moneris_cloud_exchangerate = fields.Char("ExchangeRate")

    moneris_cloud_pan = fields.Char("Pan")

    moneris_cloud_cardtype = fields.Char("Card Type")

    moneris_cloud_cardname = fields.Char("Card Name")

    moneris_cloud_accounttype = fields.Char("Account Type")

    moneris_cloud_swipeindicator = fields.Char("Swipe Indicator")

    moneris_cloud_formfactor = fields.Char("FormF actor")

    moneris_cloud_cvmindicator = fields.Char("Cvm Indicator")

    moneris_cloud_reservedfield1 = fields.Char("Reserved Field1")

    moneris_cloud_reservedfield2 = fields.Char("Reserved Field2")

    moneris_cloud_authcode = fields.Char("Auth Code ")

    moneris_cloud_invoicenumber = fields.Char("Invoice Number")

    moneris_cloud_emvechodata = fields.Char("EMV Echo Data")

    moneris_cloud_reservedfield3 = fields.Char("Reserved Field3")

    moneris_cloud_reservedfield4 = fields.Char("Reserved Field4")

    moneris_cloud_aid = fields.Char("AID")

    moneris_cloud_applabel = fields.Char("App Label")

    moneris_cloud_apppreferredname = fields.Char("App Preferred Name")

    moneris_cloud_arqc = fields.Char("Arqc")

    moneris_cloud_tvrarqc = fields.Char("TvrArqc")

    moneris_cloud_tcacc = fields.Char("Tcacc")

    moneris_cloud_tvrtcacc = fields.Char("TvrTcacc")

    moneris_cloud_tsi = fields.Char("Tsi")

    moneris_cloud_tokenresponsecode = fields.Char("Token Response Code")

    moneris_cloud_token = fields.Char("Token ")

    moneris_cloud_logonrequired = fields.Char("Logon Required")

    moneris_cloud_cncryptedcardinfo = fields.Char("Encrypted Card Info")

    moneris_cloud_transdate = fields.Char("Trans Date")

    moneris_cloud_transtime = fields.Char("Trans Time")

    moneris_cloud_amount = fields.Char("Moneris Amount")

    moneris_cloud_referencenumber = fields.Char("Reference Number")

    moneris_cloud_receiptid = fields.Char("Receipt Id")

    moneris_cloud_transid = fields.Char("Trans Id")

    moneris_cloud_timeout = fields.Char("TimedOut")

    moneris_cloud_cloudticket = fields.Char("Cloud Ticket")

    moneris_cloud_txnname = fields.Char("TxnName")

    moneris_card_type = fields.Char("Card Type ")

    is_moneriscloud_payment = fields.Boolean(
        default=False,
        compute='compute_is_moneriscloud_payment')

    attachment_id = fields.Many2one(
        string='Payment Attachment',
        comodel_name='ir.attachment',
        ondelete='restrict',
    )

    merchant_attachment_id = fields.Many2one(
        string='Payment Attachment ',
        comodel_name='ir.attachment',
        ondelete='restrict',
    )

    moneris_receipt = fields.Binary(string="Moneris Receipt", related="attachment_id.datas")

    moneris_receipt_name = fields.Char(string="Moneris Receipt Name", related="attachment_id.name")

    moneris_merchant_receipt = fields.Binary(string="Moneris Merchant Receipt", related="merchant_attachment_id.datas")

    moneris_merchant_receipt_name = fields.Char(string="Moneris Merchant Receipt Name",
                                                related="merchant_attachment_id.name")

    @api.depends('payment_method_id')
    def compute_is_moneriscloud_payment(self):
        for record in self:
            record.is_moneriscloud_payment = False
            if record.payment_method_id.use_payment_terminal == 'moneris_cloud':
                record.is_moneriscloud_payment = True


class PosOrderInherit(models.Model):
    _inherit = 'pos.order'

    payment_acquirer_name = fields.Char("Payment Acquirer Name")

    cloud_request_id = fields.Char("Cloud Request ID")

    purchase_receipt_id = fields.Char()

    moneris_cloud_cloudticket = fields.Char("Moneris Last Order Sequence")

    moneris_cloud_receiptid = fields.Char()

    moneris_cloud_transid = fields.Char()
