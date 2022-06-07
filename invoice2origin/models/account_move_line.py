# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'account.move.line'

    invoice2origin_qty = fields.Float(string='Origin Qty')
    invoice2origin_previous_ids = fields.Many2many('account.move', string='Facturas FEO')
