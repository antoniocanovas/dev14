from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    def _get_timesheet_qty(self):
        for record in self:
            total = 0
            if record.product_id.type == 'service':
                used = self.env['account.analytic.line'].search([('so_line', '=', record.id)])
                for li in used: total += li.unit_amount
            else:
                used = self.env['account.analytic.line'].search([('work_sheet_so_line_id', '=', record.id)])
                for li in used: total += li.unit_amount
            record['timesheet_qty'] = total

    timesheet_qty = fields.Float('Work Sheet', compute=_get_timesheet_qty)