# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import UserError
import logging
import requests

_logger = logging.getLogger(__name__)

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    use_clover_terminal = fields.Boolean()

    clover_server_url = fields.Char()

    clover_config_id = fields.Char('Clover Config Id',)

    clover_jwt_token = fields.Text()

    clover_merchant_id = fields.Char()

    clover_device_id = fields.Many2one(
        string='Device',
        comodel_name='clover.device',
        ondelete='restrict',
        domain=lambda self: [('journal_id', '=', self.id)],
        help="To obtain the deviceId, you must first retrieve an accessToken and your merchantId. Press 'Get Device Id' button to get the Device Id."
    )

    clover_device_name = fields.Char(
        string='Device ID', 
        related='clover_device_id.device_id' )

    clover_log_ids = fields.One2many(
        string='Clover Logs',
        comodel_name='ir.logging',
        inverse_name='journal_id',
        domain=[('journal_id', '!=', False), (('journal_id.use_clover_terminal', '=', True))]
    )
