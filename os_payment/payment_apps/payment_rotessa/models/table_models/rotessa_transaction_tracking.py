from odoo import fields, models, api
from odoo.exceptions import UserError


class RotessaTransactionTracking(models.Model):
    _name = 'rotessa.transaction.tracking'

    _description = "Rotessa Transaction Tracking"

    _rec_name = "transaction_schedule_id"

    transaction_schedule_id = fields.Integer("Transaction Schedule ID")

    invoice_no = fields.Many2one("account.move", "Invoice Number")

    invoice_ref = fields.Char("Reference")

    invoice_partner_id = fields.Many2one("res.partner", "Partner")

    invoice_date = fields.Date("Invoice Date")

    process_date = fields.Date("Process Date")

    state = fields.Selection(
        [
            ("Future", "Future"),
            ("Pending", "Pending"),
            ("Approved", "Approved"),
            ("Declined", "Declined"),
            ("Chargeback", "Chargeback"),
        ],
        "Transaction Status",
        default="Future",
    )

    status_reason = fields.Char("Status Reason")

    remain_settle_day = fields.Char("Remaining days to Settle")

    transaction_ids = fields.One2many(
        string="Transaction Ids",
        comodel_name="payment.transaction",
        inverse_name="rotessa_track_id",
    )

    transaction_id = fields.Many2one(
        "payment.transaction",
        string="Transaction Ids",
    )

    provider_id = fields.Many2one("payment.provider", "Provider")

    amount = fields.Float(string="Amount", digits=(6, 3), default=0.0)

    transaction_request_date = fields.Datetime(string="Requested time")

    last_cron_update = fields.Datetime("Last Cron Update",readonly=True)
