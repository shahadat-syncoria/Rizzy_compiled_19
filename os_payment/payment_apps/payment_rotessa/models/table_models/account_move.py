from datetime import datetime

from odoo import fields, models,  api,_
from odoo.exceptions import UserError
from odoo.addons.os_payment.payment_apps.payment_rotessa.utils.helper import _get_provider


class RotessaAccountMove(models.Model):
    _inherit = 'account.move'

    rotessa_customer_id = fields.Char(string="Rotessa Customer ID", related='partner_id.rotessa_cust_id',copy=False)

    rotessa_payment_frequency = fields.Selection([
        ("Once", "One time payment"),
        ("Weekly", "Every week"),
        ("Every_Other_Week", "Every two weeks"),
        ("Monthly", "Every month"),
        ("Every_Other_Month", "Every two months"),
        ("Quarterly", "Every 3 months"),
        ("Semi-Annually", "Every six months"),
        ("Yearly", "Once a year"),

    ], "Rotessa Payment Frequency", default="Once")

    rotessa_process_date = fields.Date(string="Rotessa process date",store=True)

    rotessa_transaction_sc_id = fields.Many2one('rotessa.transaction.tracking',readonly=True)

    rotessa_transaction_state = fields.Selection(related='rotessa_transaction_sc_id.state')

    rotessa_transaction_comment = fields.Char("Comment")

    is_rotessa_active = fields.Boolean(
        compute="_compute_is_rotessa_active",
        store=False
    )

    def _compute_is_rotessa_active(self):
        active = self._is_rotessa_active()
        for rec in self:
            rec.is_rotessa_active = active
