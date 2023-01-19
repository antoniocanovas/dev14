from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    trace_line_ids = fields.One2many('trace.line', 'sale_id')



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    trace_line_id = fields.Many2one('trace.line', string='Tracing')