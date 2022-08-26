from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    outlet = fields.Boolean('Outlet')

    vehicle_supplier_id = fields.Many2one('res.partner', string="Proveedor")
    vehicle_customer_id = fields.Many2one('res.partner', string="Comprador")
    vehicle_legal_customer_id = fields.Many2one('res.partner', string="Represent. legal")
