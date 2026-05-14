# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import logging
import json
from odoo import models, fields, api, exceptions, _
_logger = logging.getLogger(__name__)
import requests

class ShopifyConnect(models.Model):
    _inherit = 'marketplace.connector'
