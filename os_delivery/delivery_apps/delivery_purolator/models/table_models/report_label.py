# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import tools
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)

class StockPickingInherit(models.Model):    
    _inherit = 'stock.picking'

    connector_label_url = fields.Char(string='Syncoria Connector Label URL')

    purolator_return_label_url = fields.Char(string='Purolator Return Label URL')
