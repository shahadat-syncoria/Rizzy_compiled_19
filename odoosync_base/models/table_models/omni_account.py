# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import requests
import logging
from ...utils.delivery_data import DataUtils

_logger = logging.getLogger(__name__)


MODULES = {
    "is_delivery": "os_delivery",
    "is_delivery_website":"os_delivery_website",
    "is_payment":"os_payment",
    "is_payment_website":"os_payment_website",
    "is_payment_pos":"os_payment_pos"
}


class OmniAccount(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin"]

    _name = "omni.account"

    _description = "Omni Account"

    _order = "id desc"

    name = fields.Char(
        string="Instance Name",
        required=True,
        copy=False,
        index=True,
        default=lambda self: _("New"),
    )

    company_id = fields.Many2one("res.company", ondelete="restrict", required=True)

    state = fields.Selection(
        [("draft", "Not Confirmed"), ("active", "Active"), ("inactive", "Inactive")],
        default="draft",
        string="State",
    )

    client_id = fields.Char('Client Id', copy=False)

    server_url = fields.Char(required=True, copy=False)

    os_user_id = fields.Char("Username", required=True, copy=False)

    user_id = fields.Many2one('res.users', ondelete='restrict')

    token = fields.Char(required=True, copy=False)

    debug_logging = fields.Boolean()

    active = fields.Boolean(default=True)

    is_delivery = fields.Boolean(string="Delivery", tracking=True)

    is_delivery_website = fields.Boolean(string="Website Delivery", tracking=True)

    is_payment = fields.Boolean(string="Payment", tracking=True)

    is_payment_website = fields.Boolean(string="Website Payment", tracking=True)

    is_payment_pos = fields.Boolean(string="POS Payment", tracking=True)

    syncoria_pos_token = fields.Char('Syncoria POS Token', copy=False)
