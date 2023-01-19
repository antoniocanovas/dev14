from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    trace_line_ids = fields.One2many('trace.line', 'sale_id')



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    trace_line_id = fields.Many2one('trace.line', string='Tracing')

    @api.depends('product_id')
    def _get_trace_line(self):
        for record in self:
            trace_line = self.env['trace.line'].search([('sale_id','=',record.order_id.id),('product_id','=',record.product_id.id)])
            if not trace_line.id:
                trace_line = self.env['trace.line'].create({'sale_id':record.order_id.id,
                                                            'product_id':record.product_id.id,
                                                            'product_uom': record.product_id.uom_id.id})
            record['trace_line_id'] = trace_line.id
        emptylines = self.env['trace.line'].search([('sale_id','=',record.order_id.id),('sale_line_ids','=',False)])
        emptylines.unlink()
