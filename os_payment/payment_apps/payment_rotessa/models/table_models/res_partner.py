import logging

import requests

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import json
from odoo.addons.os_payment.payment_apps.payment_rotessa.utils.helper import _get_provider

_logger = logging.getLogger(__name__)


class ResPartnerBankRotessa(models.Model):
    _inherit = 'res.partner.bank'

    bank_transit_no = fields.Char(
        string="Bank Transit No",
    )


class ResPartnersRotessa(models.Model):
    _inherit = 'res.partner'

    rotessa_authorization_type = fields.Selection([("online", "Online"), ("in_person", "In Person")])

    rotessa_cust_id = fields.Char("Rotessa Customer ID")

    rotessa_bank_id = fields.Many2one('res.partner.bank', "Rotessa Bank ID", domain="[('partner_id', '=', id)]")

    rotessa_institution_number = fields.Char("Institution Number", related='rotessa_bank_id.bank_id.bic')

    rotessa_transit_number = fields.Char("Transit Number", related='rotessa_bank_id.bank_transit_no')

    rotessa_cust_identf_number = fields.Integer("Rotessa customer identification numer", related='id')

    is_rotessa_active = fields.Boolean(
        compute="_compute_is_rotessa_active",
        store=False
    )

    def _compute_is_rotessa_active(self):
        active = self._is_rotessa_active()
        for rec in self:
            rec.is_rotessa_active = active
