# Copyright 2020 Tecnativa - Antonio Cánovas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.depends('price_unit', 'price_subtotal')
    def get_purchase_net_price(self):
        for record in self:
            price = 0
            monetary_precision = self.env['decimal.precision'].sudo().search([('id', '=', 1)]).digits
            if record.price_unit != 0:
                price = round(record.price_subtotal / record.product_qty, monetary_precision)
            record['price_net'] = price
    price_net = fields.Float(
        string='Net price',
        store=True,
        compute = 'get_purchase_net_price'
    )
