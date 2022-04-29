# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
from .common import IMAGE_PLACEHOLDER

# Used to render html field in TreeView
TREE_TEMPLATE = (
    '<table style="width:100%%;border:none;" title="table">'
    "<tbody>"
    "<tr>"
    #'<td style="width: 0%%;"><img class="rounded-circle"'
    #' style="width: 64px; padding:10px;" src="data:image/png;base64,%s"'
    #' alt="Avatar" title="%s" width="100" border="0" /></td>'
    #'<td style="width: 100%%;">'
    '<td style="width: 0%%;"></td>'
    '<table style="width: 100%%; border: none;">'
    "<tbody>"
    "<tr>"
    '<td id="name" style="font-size: 16px;"><strong><span id="name">%s</span></strong>  &nbsp; <span id="responsible">[%s]</span></td></td>'
    '<td></td>'
    '<td></td>'
    '<td></td>'
    '<td id="customer" style="text-align:right;"><strong><span title="%s" id="customer">%s</span></strong></td>'
    "</tr>"
)

class ProjectProject(models.Model):
    _inherit = 'project.project'

    phase_ids = fields.One2many('project.phase', 'project_id', string='Etapas')

    project_user_avatar = fields.Binary(string="Avatar", readonly=False, related="user_id.image_128")
    project_phase_display = fields.Html(string="Project Phase", compute="_compute_project_display")

    @api.depends("phase_ids")
    def _compute_project_display(self):

        # Compose subject
        for rec in self:
            phase_template = (
                ""
            )
            #    "<tr>"
            #    '<td><strong>Responsable</strong></td>'
            #    '<td><strong>Nombre</strong></td>'
            #    '<td><strong>Tipo</strong></td>'
            #    '<td><strong>Fecha Límite</strong></td>'
            #    '<td><strong>Estado</strong></td>'
            #    '</tr>'
            #)

            for phase in rec.phase_ids:
                phase_template += (
                    '<tr>'
                    '<td style="font-size: 12px;"><strong>%s : %s</strong></td>' 
                    '<td></td>'
                    '<td style="font-size: 12px;text-align:right;"><strong>%s</strong></td>'
                    '<td style="font-size: 12px;text-align:right;"><strong>%s</strong></td>'
                    '<td style="font-size: 12px;text-align:right;"><strong>%s</strong></td>'
                    '</tr>' % (
                        phase.type,
                        phase.name,
                        phase.user_id.name,
                        phase.state,
                        phase.date_limit,
                    )
                )

            phase_template += (
                "</td>"
                "</tr>"
                "</tbody>"
                "</table>"
            )
            rec.project_phase_display = TREE_TEMPLATE % (
                #rec.project_user_avatar.decode("utf-8") if rec.project_user_avatar
                #else IMAGE_PLACEHOLDER,
                #rec.user_id.name,
                rec.name,
                rec.user_id.name if rec.user_id else '',
                rec.partner_id.name if rec.partner_id else '',
                rec.partner_id.name if rec.partner_id else '',

            ) + phase_template
