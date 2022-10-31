# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Serincloud SL
##############################################################################
from odoo import api, fields, models, _


class WorkTimesheetWizard(models.TransientModel):
    _name = "work.timesheet.wizard"
    _description = "Work Sheet Timesheet Wizard"


    name = fields.Char('Name', store=True, readonly=False)
    work_sheet_id = fields.Many2one('work.sheet', string='Sheet', store=True)
    project_id = fields.Many2one('project.project', string='Project', store=True)
    task_id = fields.Many2one('project.task', string='Task', store=True)
    time_type_id = fields.Many2one('project.time.type', string='Schedule')
    employee_ids = fields.Many2one('hr.employee', string='Employees')
    start = fields.Float('Start')
    stop = fields.Float('Stop')
    duration = fields.Float('Duration', store=True)

    timesheet_ids = fields.Many2many('account.analytic.line')

