# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import logging
import json
from odoo import models, fields, api, exceptions, _
from ast import literal_eval
import requests
logger = logging.getLogger(__name__)


class MarketplaceConnect(models.Model):
    _name = 'marketplace.connector'

    _description = 'Marketplace Connector'
