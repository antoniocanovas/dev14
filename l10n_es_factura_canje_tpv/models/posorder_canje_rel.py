# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class PosorderCanjeRel(models.Model):
    _name = 'posorder.canje.rel'

    posorder_id = fields.Many2one('pos.order', string='Pos order')
    fcanje_id =  fields.Many2one('factura.canje', string='Factura canje')