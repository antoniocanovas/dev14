# Copyright 2020 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

class PurchaseOrderLinePriceHistoryLine(models.TransientModel):
    _inherit = "purchase.order.line.price.history.line"

    discount = fields.Float(
        string='Discount',
        related='purchase_order_line_id.discount'
    )

#    @api.depends('price_unit', 'discount')
#    def get_purchase_net_price(self):
#        if self.discount:
#            self.price_net = self.price_unit
#            self.price_net = self.purchase_order_line_id.price_unit * (1 - self.purchase_order_line_id.discount/100)
#        else:
#            self.price_net = self.price_unit
    price_net = fields.Float(
        string='Net price',
        store=False,
        related = 'purchase_order_line_id.x_price_net'
    )
