from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class HrExpeseLine(models.Model):
    _name = 'hr.expense.line'
    _description = 'Hr expense detail line'

    type_id = fields.Many2one('hr.expense.type', string="Type")
    amount = fields.Float('Amount')
    expense_id = fields.Many2one('hr.expense', string='Expense', store=True, required=True)

    @api.depends('type_id')
    def get_name_from_type(self):
        name = self.name
        if self.type_id.name:
            name = self.type_id.name
        self.name = name
    name = fields.Char('Description', compute='get_name_from_type')
