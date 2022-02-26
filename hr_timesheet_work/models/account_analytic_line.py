from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    work_sheet_id = fields.Many2one('work.sheet', store=True)
    work_sheet_so_line_id = fields.Many2one('sale.order.line', store=True)

    type_id = fields.Many2one('project.time.type', 'Type', store=True)
    sale_id = fields.Many2one('sale.order', 'Sale order', store=True)
