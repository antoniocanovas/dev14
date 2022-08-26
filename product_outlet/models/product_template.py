from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    outlet = fields.Boolean('Outlet')

    outlet_supplier_id = fields.Many2one('res.partner', string="Proveedor")
    outlet_customer_id = fields.Many2one('res.partner', string="Comprador")
    outlet_legal_customer_id = fields.Many2one('res.partner', string="Represent. legal")
