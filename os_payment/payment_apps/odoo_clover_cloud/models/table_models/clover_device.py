# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import UserError
import logging
import requests
import json

_logger = logging.getLogger(__name__)



class CloverDevice(models.Model):
    _name = 'clover.device'

    _description = 'Clover Device'

    _rec_name = 'name'

    name = fields.Char(default='New Clover Device')

    device_id = fields.Char('Device Id')

    model = fields.Char()

    serial = fields.Char()

    secure_id = fields.Char('Secure Id')

    build_type = fields.Char()

    device_type_name = fields.Char()

    product_name = fields.Char()

    pin_disabled = fields.Boolean()

    offline_payments = fields.Boolean()

    offline_payments_all = fields.Boolean()

    device_status = fields.Boolean()

    x_pos_id = fields.Char()

    is_sale = fields.Boolean(string='Sale Device', default=True)

    journal_id = fields.Many2one(
        string='Journal Id',
        comodel_name='account.journal',
        ondelete='restrict',
        domain=[('use_clover_terminal','=',True)],
    )
