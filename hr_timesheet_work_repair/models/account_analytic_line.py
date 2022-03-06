from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    repair_id = fields.Many2one('repair.order', 'Repair', store=True)
