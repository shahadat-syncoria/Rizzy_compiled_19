import ast
import json
import logging

from odoo import models

_logger = logging.getLogger(__name__)


SUPPORTED_CHECKOUT_PROVIDERS = {
    'monerischeckout',
    'clover_checkout',
}

CARD_TYPE_MAP = {
    'V': 'Visa',
    'VI': 'Visa',
    'VISA': 'Visa',
    'M': 'Mastercard',
    'MC': 'Mastercard',
    'MASTERCARD': 'Mastercard',
    'MASTER CARD': 'Mastercard',
    'AX': 'American Express',
    'AMEX': 'American Express',
    'AMERICANEXPRESS': 'American Express',
    'AMERICAN EXPRESS': 'American Express',
    'DC': "Diner's Card",
    'DINERS': "Diner's Card",
    'DINERSCLUB': "Diner's Card",
    'DINERS CLUB': "Diner's Card",
    'NO': 'Novus/Discover',
    'DISCOVER': 'Discover',
    'D': 'INTERAC Debit',
    'INTERAC': 'INTERAC Debit',
    'INTERACDEBIT': 'INTERAC Debit',
    'INTERAC DEBIT': 'INTERAC Debit',
    'C1': 'JCB',
    'JCB': 'JCB',
}

TRANSACTION_CARD_SOURCE_FIELDS = (
    'moneris_card_name',
    'clover_checkout_card_brand',
    'clover_checkout_card_type',
    'bamborachk_card_type',
)

PAYMENT_CARD_SOURCE_FIELDS = (
    'moneris_cloud_cardname',
    'moneris_cloud_apppreferredname',
    'moneris_cloud_applabel',
    'moneris_cloud_cardtype',
    'clover_card_type',
    'clover_type',
)

PAYMENT_CARD_TRIGGER_FIELDS = set(PAYMENT_CARD_SOURCE_FIELDS) | {
    'payment_transaction_id',
    'payment_method_line_id',
    'journal_id',
    'memo',
    'move_id',
    'clover_transaction_info',
    'clover_response',
}


class AccountPayment(models.Model):
    _inherit = 'account.payment'
