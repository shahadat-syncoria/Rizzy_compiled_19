# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, exceptions, _
import logging
import json
import requests
from pprint import pprint

_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    use_cloud_terminal = fields.Boolean()

    cloud_store_id = fields.Char(
        "Moneris Store ID", help="Unique identifier provided by Moneris upon merchant account setup", )

    cloud_api_token = fields.Char(
        "Moneris API Token", help="Unique alphanumeric string assigned by Moneris upon merchant account activation", )

    cloud_terminal_id = fields.Char(
        "Moneris Terminal ID", help="The ECR number of the particular PINpad you are addressing", )

    cloud_pairing_token = fields.Char(
        "Moneris Pairing Token", help="The ECR number of the particular PINpad you are addressing",)

    cloud_postback_url = fields.Char(
        "Moneris Postback URL", help="Value provided by the terminal as part of the pairing process")

    cloud_integration_method = fields.Selection([
        ('postbackurl', 'Postback URL'),
        ('polling', 'Cloud HTTPS Polling'),
        ('combined', 'Combined')],
        required=True, default='polling', copy=False, store=True, readonly=True)

    cloud_cloud_environment = fields.Selection([
        ('enabled', 'Enabled'),
        ('test', 'Test Mode')], string="Moneris Cloud Environment", default='test', copy=False, store=True)

    cloud_cloud_paired = fields.Boolean("Moneris Cloud Paired", default=False)

    cloud_cloud_ticket = fields.Boolean("Moneris Cloud Ticket", default=False)

    cloud_inout_url = fields.Char("cloud_inout_url", store=True)

    cloud_out_url1 = fields.Char("cloud_out_url1", store=True)

    cloud_out_url2 = fields.Char("cloud_out_url2", store=True)

    cloud_merchant_id = fields.Char()

    is_moneris_go_cloud = fields.Boolean("Is Moneris Go Cloud?", default=False)
