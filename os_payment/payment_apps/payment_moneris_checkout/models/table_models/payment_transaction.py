# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import logging
import pprint

from odoo import api, models
from odoo.exceptions import UserError, ValidationError
from odoo.http import request
from odoo.addons.payment import utils as payment_utils
from odoo.addons.odoosync_base.utils.helper import convert_curency

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'
        
    ###########################################################################################
    ###########################################################################################
