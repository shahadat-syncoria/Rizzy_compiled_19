import logging
from dateutil import parser
from odoo import fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError
import time

_logger = logging.getLogger(__name__)


class ResolvepayFetchWizard(models.Model):
    _name = 'resolvepay.fetch.wizard'

    _description = 'Fetch Customer'

    instance_id = fields.Many2one(
        string='ResolvePay Instance',
        comodel_name='resolvepay.instance',
    )

    create_new = fields.Boolean(string='Create New Contact If Not Found')

    status = fields.Selection([('all', 'All'), ('active', 'Active'), ('archived', 'Archived')], 'Status', default='all')
