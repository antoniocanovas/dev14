# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
from .common import IMAGE_PLACEHOLDER

# Used to render html field in TreeView
TREE_TEMPLATE = (
    '<table style="width:100%%;border:none;" title="table">'
    "<tbody>"
    "<tr>"
    '<td style="width: 15%%;"><strong>%s</strong></td>'
    '<td style="width: 85%%;">'
    '<table style="width: 100%%; border: none;">'
    "<tbody>"
    "<tr>"
    '<td id="name"><strong><span id="name">%s</span></strong></td>'
    "<td></td>"
    "</tr>"
    "<tr>"
    '<td id="description"><span id="description">%s</span></td>'
    "<td></td>"
    "</tr>"
    "</tbody>"
    "</table>"
)

class ProjectProject(models.Model):
    _inherit = 'project.project'

    phase_ids = fields.One2many('project.phase', 'project_id', string='Etapas')

    project_phase_display = fields.Html(string="Project Phase", compute="_compute_project_display")

    @api.depends("phase_ids")
    def _compute_project_display(self):

        # Compose subject
        for rec in self:
            phase_template = (
                '<table style="width:100%%;border:none;" title="table">'
                "<tbody>"
                "<tr>"
                '<td style="width: 20%%;"><strong>Responsable</strong></td>'
                '<td style="width: 20%%;"><strong>Nombre</strong></td>'
                '<td style="width: 20%%;"><strong>Tipo</strong></td>'
                '<td style="width: 20%%;"><strong>Fecha Límite</strong></td>'
                '<td style="width: 20%%;"><strong>Estado</strong></td>'
                '</tr>'

            )

            for phase in rec.phase_ids:
                phase_template += (
                    '<tr>'
                    '<td style="width: 20%%;"><strong>%s</strong></td>' 
                    '<td style="width: 20%%;"><strong>%s</strong></td>'
                    '<td style="width: 20%%;"><strong>%s</strong></td>'
                    '<td style="width: 20%%;"><strong>%s</strong></td>'
                    '<td style="width: 20%%;"><strong>%s</strong></td>'
                    '</tr>' % (
                        phase.user_id.name,
                        phase.name,
                        phase.type,
                        phase.date_limit,
                        phase.state,
                    )
                )

            phase_template += (
                "</tbody>"
                "</table>"
                "</td>"
                "</tr>"
                "</tbody>"
                "</table>"
            )

            rec.project_phase_display = TREE_TEMPLATE % (
                "REC PYTO",
                rec.name,
                rec.description if rec.description else "",

            ) + phase_template
