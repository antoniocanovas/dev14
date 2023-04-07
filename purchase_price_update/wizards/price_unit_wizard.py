# Copyright

import base64
import codecs
from PIL import Image
import io
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PriceUnitInfo(models.TransientModel):
    _name = 'price.unit.info'
    _description = 'Pop up if price/unit is changed'

    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order')
    message = fields.Char(string='Message')

    def update_product_standard_price(self):
        self.ensure_one()
        self.purchase_order_id.update_product_standard_price()