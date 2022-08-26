from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    invoice_id = fields.Many2one("account.move",
                                       related="move_id.move_id",
                                       string="Invoice")
