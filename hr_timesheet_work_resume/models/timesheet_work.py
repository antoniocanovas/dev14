# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class TimesheetWork(models.Model):
    _name = 'timesheet.work'

    sale_order_ids = fields.Many2many('sale.order', string='Sale Orders')
    todo_ids = fields.One2many('timesheet.line.todo', 'work_id')

    @api.depends('todo_ids')
    def get_todo_count(self):
        for record in self:
            record.todo_count = len(record.todo_ids.ids)
    todo_count = fields.Integer(string='To-do', store=False, compute='get_todo_count',)
