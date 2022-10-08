from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    work_sheet_id = fields.Many2one('work.sheet', store=True)
    set_start_stop = fields.Boolean(related='work_sheet_id.set_start_stop', string='Set start & stop time', store=False)

    def get_self_id(self):
        for record in self:
            record['self_id'] = record.id
    self_id = fields.Many2one('account.analytic.line', string='Name ID', compute='get_self_id')