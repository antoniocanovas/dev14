from odoo import _, api, fields, models


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    line_ids = fields.One2many('hr.expense.line', 'expense_id', string="Detail", store=True)

    @api.depends('line_ids.amount', 'line_ids')
    def get_lines_amount(self):
        total = 0
        for li in self.line_ids:
            total += li.amount
        self.line_amount = total
    line_amount = fields.Float('Detail total', store=True, compute='get_lines_amount')
