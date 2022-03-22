# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    bulk_id = fields.Many2one('product.product',string='Bulk')
    bulk_uom_id = fields.Many2one('uom.uom',string='Uom', related='bulk_id.uom_po_id')
    bulk_ratio = fields.Float(string='Ratio')



