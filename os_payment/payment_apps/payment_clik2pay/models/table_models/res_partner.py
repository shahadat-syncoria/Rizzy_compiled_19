# -*- coding: utf-8 -*-


import random
import string
import re
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    merchantAccountId = fields.Char(string="Merchant Account ID", readonly=True, copy=False)
