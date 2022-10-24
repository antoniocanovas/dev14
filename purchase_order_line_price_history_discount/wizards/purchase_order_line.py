# Copyright 2020 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

class MailMessage(models.Model):
    _inherit = "purchase.order.line"

    @api.depends('price_unit', 'price_subtotal')
    def get_purchase_net_price(self):
        price = 0
        monetary_precision = self.env['decimal.precision'].sudo().search([('id', '=', 1)]).digits
        if self.price_unit != 0:
            price = round(self.price_subtotal / self.product_qty, monetary_precision)
        self.write.price_net = price
    price_net = fields.Float(
        string='Net price',
        store=True,
        compute = 'get_purchase_net_price'
    )
