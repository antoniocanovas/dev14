# Copyright 2020 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

class PurchaseOrderLinePriceHistoryLine(models.TransientModel):
    _inherit = "purchase.order.line.price.history.line"

    discount = fields.Float(
        string='Discount',
        store=False,
        related='purchase_order_line_id.discount'
    )

    price_net = fields.Float(
        string = 'Net price',
        store = False,
        related = 'purchase_order_line_id.price_net'
    )

    product_oum = fields.Char(
        string = 'UOM',
        store = False,
        related = 'purchase_order_line_id.product_uom.name'
    )