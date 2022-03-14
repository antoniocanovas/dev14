# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectProcedureLine(models.Model):
    _name = 'project.procedure.line'
    _description = 'Líneas de procedimiento de proyecto.'


    type_id = fields.Many2one('project.procedure',string='Tipo')
    procedure_id = fields.Many2one('project.procedure.action',
                                 domain=[('active','=',True)],string='Acción',required=True)
    dependency_ids = fields.Many2many('project.procedure.action',
                                 domain=[('active', '=', True)], string='Dependencia')

    def compute_get_name(self):
        for record in self:
            record['name'] = record.type_id.name + " => " + record.procedure_id.name

    name = fields.Char(string='Nombre', compute=compute_get_name, required=True, readonly=True)

    @api.depends('procedure_id')
    def compute_get_user(self):
        for record in self:
            record['user_id'] = record.procedure_id.user_id.id

    user_id = fields.Many2one('res.users', compute=compute_get_user, string='Usuario')

    @api.depends('procedure_id')
    def compute_get_departament(self):
        for record in self:
            record['departament_id'] = record.procedure_id.departament_id.id

    departament_id = fields.Many2one('hr.department',compute=compute_get_departament, string='Departamento')

    @api.depends('procedure_id')
    def compute_get_interval(self):
        for record in self:
            record['interval'] = record.procedure_id.interval

    interval = fields.Integer(string='Intervalo',compute=compute_get_interval)