from odoo import _, api, fields, models

import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    timesheet_todo_ids = fields.One2many('timesheet.line.todo', 'sale_id')
    timesheet_done_ids = fields.One2many('timesheet.line.done', 'sale_id')

    @api.depends('timesheet_todo_ids')
    def get_timesheet_done_count(self):
        for record in self:
            record.timesheet_todo_count = len(record.timesheet_todo_ids.ids)
    timesheet_todo_count = fields.Float('To-do', store=False, compute='get_timesheet_done_count')


    @api.depends('timesheet_done_ids')
    def get_timesheet_done_count(self):
        for record in self:
            record.timesheet_done_count = len(record.timesheet_done_ids.ids)
    timesheet_done_count = fields.Float('Done', store=False, compute='get_timesheet_done_count')
