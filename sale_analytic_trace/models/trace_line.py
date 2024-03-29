from odoo import _, api, fields, models


class TraceLine(models.Model):
    _name = 'trace.line'
    _description = 'Sale Analtyic Line'

    name = fields.Char('Name', related='product_id.name', store=True, readonly=True)
    sale_id = fields.Many2one('sale.order', string='Sale', store=True, readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Account', related='sale_id.analytic_account_id')
    product_id = fields.Many2one('product.product', string='Product')
    estimated_qty = fields.Float('Qty')
    consumed_qty = fields.Float('Consumed')
    product_uom = fields.Many2one('uom.uom', string='Uom')
    sale_line_ids = fields.One2many('sale.order.line', 'trace_line_id', string='Sale lines', store=True, readonly=True)