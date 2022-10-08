# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Serincloud SL
##############################################################################
from odoo import api, fields, models, _


class TimesheetLineTodo(models.Model):
    _name = "timesheet.line.todo"
    _description = "Timesheet Line To-Do"

    active = fields.Boolean('Active',default=True)
    work_id = fields.Many2one('timesheet.work', store=True, string='Work')
    sale_line_id = fields.Many2one('sale.order.line', store=True, string='Sale Line')

    @api.depends('sale_line_id')
    def get_todo_product(self):
        for record in self:
            record.product_id = record.sale_line_id.product_id.id
    product_id = fields.Many2one('product.product', string='Product', required=True, readonly=False,
                                 compute='get_todo_product',)

    @api.depends('product_id')
    def get_todo_name(self):
        for record in self:
            record.name = record.product_id.name
    name = fields.Char(string='Name', compute='get_todo_name', readonly=False, store=True)

    @api.depends('product_id')
    def get_todo_uom(self):
        for record in self:
            record.uom_id = record.product_id.uom_id.id
    uom_id = fields.Many2one(string='UOM', compute='get_todo_uom', store=True)

