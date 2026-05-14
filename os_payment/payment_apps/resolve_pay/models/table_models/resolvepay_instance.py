from odoo import models, fields, api, _
import requests
from odoo.exceptions import UserError, ValidationError
from requests.auth import HTTPBasicAuth
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)
from odoo.addons.odoosync_base.utils.app_payment import AppPayment


class ResolvePay(models.Model):
    _name = 'resolvepay.instance'

    _description = 'Resolvepay Instance'

    name = fields.Char(string='Instance Name', default='ResolvePay', required=True)

    token = fields.Char(string='Token')

    company_id = fields.Many2one('res.company', required=True)

    connect_state = fields.Selection([
        ('draft', 'Not Confirmed'),
        ('confirm', 'Confirmed')],
        default='draft', string='State')

    journal_id = fields.Many2one('account.journal', string='Journal')

    template_id = fields.Many2one('ir.actions.report', string='PDF to Send', help='This PDF version will be sent when submitting an invoice', domain=[('model', '=', 'account.move')])

    _sql_constraints = [
        ('instance_name_uniq', 'unique (name)', 'Instance name must be unique.')
    ]
