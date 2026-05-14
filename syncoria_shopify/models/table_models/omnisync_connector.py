# -*- coding: utf-8 -*-
###############################################################################
#    Harden omnisync_api_call for Shopify flows without changing odoosync_base.
###############################################################################

from odoo import models


class OmnisyncConnector(models.Model):
    _inherit = 'omnisync.connector'
