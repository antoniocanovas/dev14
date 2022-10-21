# Copyright 2020 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

class PurchaseOrderLinePriceHistoryLine(models.TransientModel):
    _inherit = "purchase.order.line.price.history.line"

    discount = fields.Float(
        string='Disc.',
        related='purchase_order_line_id.discount'
    )

    @api.depends('price_unit', 'discount')
    def get_purchase_net_price(self):
        self.price_net = self.price_unit * (1 - self.discount/100)
    price_net = fields.Monetary(
        string='Net price',
        store=False,
        compute='get_purchase_net_price',
    )
