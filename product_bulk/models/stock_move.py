# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    bulk_line_id = fields.Many2one('stock.move',string='Bulk line')
    bulk_avco_done = fields.Boolean('AVCO done')