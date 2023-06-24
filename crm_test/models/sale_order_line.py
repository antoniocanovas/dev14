from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    order_line = fields.One2many('sale.order.line', 'order_id', 'Order Lines', limit=200)