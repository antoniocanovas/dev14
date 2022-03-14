# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class Stock.Picking(models.Model):
    _inherit = 'stock.picking'

    project_phase_id = fields.Many2one('project.phase',string='Fase')



