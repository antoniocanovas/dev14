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
    line_amount = fields.Float('Detail total', store=False, compute='get_lines_amount')

    @api.depends('line_ids.amount', 'line_ids')
    def get_lines_amount_estimation(self):
        total = 0
        for li in self.line_ids:
            if li.type_id.amount > li.amount:
                total += li.type_id.amount
            else:
                total += li.amount
        self.market_amount = total
    market_amount = fields.Float('Market estimation', store=False, compute='get_lines_amount_estimation')
