from odoo import _, api, fields, models
from datetime import datetime, timezone, timedelta
import pytz
import base64
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class ProductDictionary(models.Model):
    _name = 'product.dictionary'
    _description = 'Product Dictionary'

    name = fields.Char('Name', required=True)
    categ_id = fields.Many2one('product.category', string='Categoría de producto', store=True, copy=True)
    type = fields.Selection([('product','Producto'),('consu','Consumible'),('service','Servicio')], store=True,
                            default='product', copy=True)