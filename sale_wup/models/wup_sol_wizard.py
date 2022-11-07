# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Serincloud SL
##############################################################################
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WupSolWizard(models.TransientModel):
    _name = "wup.sol.wizard"
    _description = "WUP New Sale Order Line add Wizard"

    sale_id = fields.Many2one('sale.order')
    analytic_line_ids = fields.Many2many('account.analytic.line', related='sale_id.product_consumed_ids')
    analytic_line_selection_ids = fields.Many2many('account.analytic.line', string="Selecteds")



#    @api.depends('version')
#    def get_work_sheet_timesheets(self):
#        self.timesheet_ids = [(6,0,self.work_sheet_id.project_service_ids.ids)]
#    timesheet_ids = fields.Many2many('account.analytic.line', store=True, readonly=False,
#                                     compute="get_work_sheet_timesheets")

    def create_sale_order_lines(self):
        picking = 0
        for aal in record.product_consumed_ids:
            svl = env['stock.valuation.layer'].search([('analytic_id', '=', aal.id)])
            sm = svl.stock_move_id
            if (svl.id) and not (sm.sale_line_id.id):
                newsol = env['sale.order.line'].create({
                    'order_id': record.id,
                    'product_id': sm.product_id.id,
                    'product_uom_qty': sm.quantity_done,
                })
                picking = newsol.move_ids[0].picking_id
                for li in newsol.move_ids:
                    li['state'] = 'draft'
                    li.unlink()
                sm['sale_line_id'] = newsol.id
                newsol['qty_delivered'] = sm.quantity_done
        if (picking != 0) and (not picking.move_ids_without_package.ids):
            picking['state'] = 'cancel'



#            new.write({'time_start':record.start, 'time_stop':record.stop, 'unit_amount':duration})
#                    record['version'] = record.version + 1
#        return {
#            'name': 'Work Sheet Add Timesheet wizard view',
#            'view_type': 'tree',
#            'view_mode': 'form',
#            'res_model': 'work.timesheet.wizard',
#            'type': 'ir.actions.act_window',
#            'view_id':
#                self.env.ref('hr_timesheet_work.work_timesheet_wizard_default_form').id,
#            'context': dict(self.env.context),
#            'target': 'new',
#            'res_id': self.id,
#        }
