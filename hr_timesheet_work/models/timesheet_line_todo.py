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

    name = fields.Char(string='Name', store=True)
    active = fields.Boolean('Active',default=True)
    work_id = fields.Many2one('timesheet.work', store=True, string='Work')
    sale_line_id = fields.Many2one('sale.order.line', store=True, string='Sale Line')
    sale_id = fields.Many2one('sale.order', related='sale_line_id.order_id', store=True)
    sale_order_ids = fields.Many2many('sale.order',related='work_id.sale_order_ids', store=False)
    product_id = fields.Many2one('product.product', string='Product', required=True, readonly=False)
    uom_id = fields.Many2one('uom.uom', string='UOM', store=True)

    # It will be executed from AA, it can't be compute because always null on save line:
    def get_update_work_todo_line(self):
        for record in self:
            name, product = "", False
            if (record.product_id.id) and:
                record.write({'product_id': record.product_id.id, 'name':record.product_id.name, 'uom_id': product.uom_id.id})
            if record.sale_line_id.id:
                record.write({'product_id': record.sale_line_id.product_id.id, 'name':record.sale_line_id.name, 'uom_id': record.sale_line_id.uom_id.id})
    # - - - - - -

