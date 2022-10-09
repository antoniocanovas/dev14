# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Serincloud SL
##############################################################################
from odoo import api, fields, models, _


class TimesheetLineDone(models.Model):
    _name = "timesheet.line.done"
    _description = "Timesheet Line Done"

    todo_id = fields.Many2one(
        'timesheet.line.todo',
        string='Item',
        required=True,
    )
    qty = fields.Integer(string='Quantity', required="1")
    uom_id = fields.Many2one('uom.uom', store=True, string='UOM', related='todo_id.uom_id')
    work_sheet_id = fields.Many2one('work.sheet', string='Sheet', store=True)
    sale_line_id = fields.Many2one('sale.order.line', string='Sale line', store=True, related='todo_id.sale_line_id')
    sale_id = fields.Many2one('sale.order', string='Sale order', store=True, related='todo_id.sale_id')
    date = fields.Date(string='Date', store=True, related='work_sheet_id.date' )

    @api.depends('todo_id')
    def get_done_name(self):
        for record in self:
            record.name = record.todo_id.name
    name = fields.Char(string='Description', compute='get_done_name', readonly=False, store=True, required="1")

