from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    trace_line_ids = fields.One2many('trace.line', 'sale_id')



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    trace_line_id = fields.Many2one('trace.line', string='Tracing')

    @api.depends('product_uom','product_uom_qty')
    def _get_units_standard(self):
        for record in self:
            standard_qty = record.product_uom_qty
            ratio = 1
            if (record.product_uom.id != record.product_id.uom_id.id):
                # uom_type: bigger, reference, smaller
                if record.product_id.uom_id.uom_type == 'smaller':
                    ratio = ratio * record.product_id.uom_po_id.factor
                elif record.product_id.uom_id.uom_type == 'bigger':
                    ratio = ratio / record.product_id.uom_po_id.factor_inv
                if record.product_uom.uom_type == 'smaller':
                    ratio = ratio / record.product_uom.factor
                elif record.product_uom.uom_type == 'bigger':
                    ratio = ratio * record.product_uom.factor_inv
            record['standard_qty'] = standard_qty * ratio
    standard_qty = fields.Float('Standard Qty', store=True, readonly=True, compute='_get_units_standard')

    def _get_trace_line(self):
        for record in self:
            if record.bom_ids.ids:
                bom = record.bom_ids[0]
                for li in bom:
                    # Pasar por todas las líneas y crear nuevos registros. También escribir en li el SO ...:
                    a=1
            else:
                trace_line = self.env['trace.line'].search([('sale_id','=',record.order_id.id),('product_id','=',record.product_id.id)])
                if not trace_line.id:
                    trace_line = self.env['trace.line'].create({'sale_id':record.order_id.id,
                                                                'product_id':record.product_id.id,
                                                                'product_uom': record.product_id.uom_id.id})
                record.write({'trace_line_id':trace_line.id})
        emptylines = self.env['trace.line'].search([('sale_id','=',record.order_id.id),('sale_line_ids','=',False)])
        emptylines.unlink()
