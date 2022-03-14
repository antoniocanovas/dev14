# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectProcedure(models.Model):
    _name = 'project.procedure'
    _description = 'Plantillas de procedimiento de proyectos'


    name = fields.Char(string='Nombre', required=True)
    line_ids = fields.One2many('project.procedure.line', 'type_id', string='Líneas')
    state = fields.Selection(
        [('borrador', 'Borrador'), ('activo', 'Activo'), ('archivado', 'Archivado')], default='borrador',
        string='Estado')
    departament_id = fields.Many2one('hr.department', string='Departamento', required=True)
    task_name = fields.Char('Nombre tarea')
    stage_ids = fields.Many2many('project.task.type')
