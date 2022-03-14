# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    project_phase_id = fields.Many2one('project.phase',string='Fase')



