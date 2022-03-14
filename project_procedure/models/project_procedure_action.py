# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectProcedureAction(models.Model):
    _name = 'project.procedure.action'
    _description = 'Acciones'

    name = fields.Char(string='Nombre',required=True)
    task_description = fields.Text('Procedimiento')
    active = fields.Boolean(string='Activo', default=True)
    departament_id = fields.Many2one('hr.department',string='Departamento')
    interval = fields.Integer('Días desde inicio exp.')
    user_id = fields.Many2one('res.users',string='usuario')
