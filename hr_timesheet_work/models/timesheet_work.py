from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


TYPES = [
    ('project', 'Project'),
]


class TimesheetWork(models.Model):
    _name = 'timesheet.work'
    _description = 'Timesheet Work'

    name = fields.Char('Name', required=True)
    active = fields.Boolean(string="Active", default=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    type = fields.Selection([('project','Project')],
        required=True, string='Type', default='project', index=True, copy=False, tracking=True)
    project_id = fields.Many2one('project.project')
    set_start_stop = fields.Boolean('Set start & stop time')
    sale_order_ids = fields.Many2many('sale.order', string='Sale Orders')
    todo_ids = fields.One2many('timesheet.line.todo', 'work_id')

    @api.depends('name')
    def get_todo_count(self):
        for record in self:
            name = "/"
            if record.name: name = record.name
            record.description = name
    description = fields.Char('Description', store=False, compute='get_task_name')

    @api.depends('todo_ids')
    def get_todo_count(self):
        for record in self:
            record.todo_count = len(record.todo_ids.ids)
    todo_count = fields.Integer(string='To-do', store=False, compute='get_todo_count',)
