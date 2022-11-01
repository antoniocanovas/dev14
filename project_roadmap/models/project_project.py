# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class ProjectProject(models.Model):
    _inherit = 'project.project'

    roadmap_ids = fields.One2many('project.roadmap','project_id', store=True)

    @api.depends("roadmap_ids")
    def _compute_roadmap_count(self):
        self.roadmap_count = len(self.roadmap_ids)
    roadmap_count = fields.Integer('Roadmaps', compute="_compute_roadmap_count", store=True)
