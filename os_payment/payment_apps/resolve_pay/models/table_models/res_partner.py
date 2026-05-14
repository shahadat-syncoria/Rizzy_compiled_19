from odoo import models, fields, api, _
import requests
from odoo.exceptions import UserError, ValidationError
import json, time
from requests.auth import HTTPBasicAuth

import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    resolvepay_id = fields.Char(string='ResolvePay Customer Id', copy=False, tracking=True)

    resolvepay_created_at = fields.Char(string='Date the customer was created.')

    resolvepay_updated_at = fields.Char(string='Date the customer was last updated.')

    resolvepay_source = fields.Char(string='ResolvePay Source')

    resolvepay_business_address = fields.Char(string='Street address of the business primary location.')

    resolvepay_business_city = fields.Char(string='City of the business primary location.')

    resolvepay_business_state = fields.Char(string='State or province of the business primary location.')

    resolvepay_business_zip = fields.Char(string='US zip code of the business primary location.')

    resolvepay_business_country = fields.Char(string='Country of the business primary location according to the ISO 3166-1 alpha 2 standard.')

    resolvepay_business_age_range = fields.Char(string='String indicating age of the business in years.')

    resolvepay_business_ap_email = fields.Char(string='Email address of the business accounts payable person or department.')

    resolvepay_business_ap_phone = fields.Char(string='Phone number of the business accounts payable person or department.')

    resolvepay_business_name = fields.Char(string='Full legal name of the business being applied for.')

    resolvepay_business_trade_name = fields.Char(string='Trade name of the business')

    resolvepay_business_phone = fields.Char(string='Phone number of the business primary location.')

    resolvepay_business_type = fields.Char(string='String indicating the business type of legal entity.')

    resolvepay_email = fields.Char(string='Email of the customer applying for terms.')

    resolvepay_personal_name_first = fields.Char(string='First name of the person applying on behalf of the business.')

    resolvepay_personal_name_last = fields.Char(string='Last name of the person applying on behalf of the business.')

    resolvepay_personal_phone = fields.Char(string='Personal phone number of the customer representative applying for terms.')

    resolvepay_amount_approved = fields.Float(string='Total amount of the credit approved.')

    resolvepay_amount_authorized = fields.Float(string='Amount of the credit line reserved for authorized charges.')

    resolvepay_amount_available = fields.Float(string='Current amount of the credit line available for purchases.')

    resolvepay_amount_balance = fields.Float(string='Current balance on the customer credit line.')

    resolvepay_amount_unapplied_payments = fields.Float(string='Current amount of a customer unapplied payments.')

    resolvepay_default_terms = fields.Selection(selection=[
        ('net7', 'net7'),
        ('net10', 'net10'),
        ('net10th', 'net10th'),
        ('net15', 'net15'),
        ('net30', 'net30'),
        ('net45', 'net45'),
        ('net60', 'net60'),
        ('net75', 'net75'),
        ('net90', 'net90'),
        ('net120', 'net120'),
        ('net180', 'net180')],
        string='Set default terms that will apply to this customer invoices. Can be overridden when requesting an advance.', tracking=True)

    resolvepay_advance_rate = fields.Float(string='Advance Rate (%)', tracking=True, help='The advance rate that will be used to determine the amount advanced for this customer invoices.')

    resolvepay_credit_status = fields.Char(string='Current credit status of this customer', tracking=True)

    resolvepay_net_terms_status = fields.Char(string='Current net terms enrollment status of this customer.', tracking=True)

    resolvepay_net_terms_enrollment_url = fields.Char(string='The URL for a customer to complete enrollment requirements when net_terms_status is pending_enrollment.')

    resolvepay_net_terms_enrollment_expires_at = fields.Char(string='The date by which the customer must be enrolled in this net terms offer')

    resolvepay_credit_check_requested_at = fields.Char(string='The date a credit check was requested.')

    resolvepay_archived = fields.Char(string='Indicating if customer is archived.', tracking=True)
