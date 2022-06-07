# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice2origin_previous_ids = fields.Many2many('account.move', string='Facturas FEO')
