# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class ProjectTask(models.Model):
    _inherit = 'project.task'

    project_phase_id = fields.Many2one('project.phase',string='Fase')



