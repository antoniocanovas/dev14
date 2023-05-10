# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Serincloud SL
##############################################################################
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WorkTimesheetWorkgroup(models.Model):
    _name = "work.timesheet.workgroup"
    _description = "Work Sheet Timesheet Workgroup"


    name = fields.Char('Name', store=True, readonly=False, required=True)
    work_sheet_id = fields.Many2one('work.sheet', string='Work Sheet', readonly=True)
    analytic_line_ids = fields.One2many('account.analytic.line', 'workgroup_id', string='Timesheets')
    task_ids = fields.Many2many('project.task', string='Tasks')
    employee_ids = fields.Many2many('hr.employee', string='Employees')
    date = fields.Date('Date', store=True, required="1")

    @api.depends('analytic_line_ids.unit_amount', 'analytic_line_ids.time_type_id')
    def _get_hour_laboral(self):
        total = 0
        for li in self.analytic_line_ids:
            if li.time_type_id.extra == False:
                total += li.unit_amount
        self.hour_laboral = total
    hour_laboral = fields.Float('Laboral hours', store=False, compute='_get_hour_laboral')

    def _get_hour_extra(self):
        total = 0
        for li in self.analytic_line_ids:
            if li.time_type_id.extra == True:
                total += li.unit_amount
        self.hour_extra = total
    hour_extra   = fields.Float('Extra hours', store=False, compute='_get_hour_extra')
