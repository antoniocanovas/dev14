# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
import datetime

class ProjectProject(models.Model):
    _inherit = 'project.project'

    phase_ids = fields.One2many('project.phase', 'project_id', string='Etapas')

