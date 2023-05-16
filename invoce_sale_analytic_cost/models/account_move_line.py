from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    analytic_cost_id = fields.Many2one('account.analytic.line', 'Analytic cost')
