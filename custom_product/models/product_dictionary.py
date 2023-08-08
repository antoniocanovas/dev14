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
