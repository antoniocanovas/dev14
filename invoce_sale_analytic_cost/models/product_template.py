from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    autoanalytic = fields.Boolean('Auto analytic cost', default=True)
