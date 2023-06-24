from odoo import _, api, fields, models


class Lead2opportunity(models.TransientModel):
    _inherit = 'sale.order.line'

    order_line = fields.One2many('sale.order.line', 'order_id', 'Order Lines', limit=200)