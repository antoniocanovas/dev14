from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

VALUES = [
    ('fixed_service_margin_over_cost', 'Our services with fixed price, and margin over cost for others.'),
    ('margin_over_cost', 'Margin over cost.'),
    ('target_price', 'Target price.'),
]


class WupSaleOrder(models.Model):
    _inherit = 'sale.order'

    target_price = fields.Monetary('Target price', currency_field='currency_id')
    price_our_service = fields.Monetary(string='Price our service')
    margin = fields.Float('Margin')
    discount_type = fields.Selection(
        selection=VALUES, string="Type",
    )
