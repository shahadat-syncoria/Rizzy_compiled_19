# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
import json

from odoo import models, _, api
from odoo.tools import float_compare


SUPPORTED_CLOUD_TERMINALS = {
    'moneris_cloud',
    'moneris_cloud_go',
    'clover_cloud',
}


class SyncoriaConnectorPosSession(models.Model):
    _inherit = 'pos.session'
