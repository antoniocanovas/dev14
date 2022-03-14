# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
import datetime

class project(models.Model):
    _inherit = 'project.project'

    is_procedure = fields.Boolean(string='Basado en procedimiento')
    procedure_id = fields.Many2one('project.procedure',domain=[('state','=','activo')],string='Plantilla')
    departament_id = fields.Many2one('hr.department',string='Departamento')
    gap_ids = fields.One2many('project.product.gap', 'project_id', string='Etapas')

    def compute_get_task(self):
        for record in self:
            tareas = self.env['project.task'].search(
                [('project_id', '=', record.id), '|', ('active', '=', False), ('active', '=', True)])
            record['task_ids'] = [(6, 0, tareas.ids)]

    task_ids = fields.Many2many('project.task', string='tarea', compute=compute_get_task, store=False)

    def make_procedure(self):
        self.is_procedure = True

    def create_case_tasks(self):
        for record in self:
            # Crear las tareas en base al tipo de procedure, enlazando cada tarea con su línea origen:
            # Si las tareas están archivadas y pulsamos de nuevo las repite, así que lo primero, sacar del archivo:
            exist = self.env['project.task'].search(
                [('project_id', '=', record.id), '|', ('active', '=', False), ('active', '=', True)])

            # Crear o actualizar añadiendo las etapas que faltan en el proyecto:
            #etapas_plantilla = record.procedure_id.stage_ids
            #for etapa in etapas_plantilla:
            #    record['type_ids'] = [(4, etapa.id)]

            # Crear o actualizar añadiendo las etapas que faltan en el proyecto:
        
            for e in record.procedure_id.stage_ids:
                record['type_ids'] = [(4, e.id)]

            # Las líneas del tipo de procedure que ya tienen tarea son:
            lineswithtask = []
            for ta in exist:
                if ta.procedure_line_id.id:
                    lineswithtask.append(ta.procedure_line_id.id)
            #
            # Buscamos las tareas que tendrían que haber y las creamos (por si se han borrado o ampliado el ámbito):
            for li in record.procedure_id.line_ids:
                if li.id not in lineswithtask:
                    nombre = record.name + " - " + li.procedure_id.name
                    nuevatarea = self.env['project.task'].create({'name': nombre,
                                                                  'project_id': record.id,
                                                                  'user_id': li.procedure_id.user_id.id,
                                                                  'departament_id': li.procedure_id.departament_id.id,
                                                                  'description': li.procedure_id.task_description,
                                                                  'active': True,
                                                                  'procedure_line_id': li.id})

            # Ahora las dependencias ya que tenemos todas las tareas de las líneas y podemos relacionar:
            todas = self.env['project.task'].search(
                [('project_id', '=', record.id), '|', ('active', '=', False), ('active', '=', True)])
            for ta in todas:
                if ta.procedure_line_id.dependency_ids.ids:
                    dependencias = []
                    for de in ta.procedure_line_id.dependency_ids:
                        tarea = self.env['project.task'].search(
                            [('procedure_line_id.procedure_id', '=', de.id), ('project_id', '=', record.id), '|',
                             ('active', '=', False), ('active', '=', True)])
                        dependencias.append(tarea.id)
                    ta['dependency_task_ids'] = [(6, 0, dependencias)]


                    # Archivar las nuevas tareas que tengan dependencias no cumplidas, por si se pulsa por segunda vez el botón "Actualizar trámites":
                    # Respeta las existentes de antes por si hemos querido adelantar algún trámite manualmente:
                if (ta.id not in exist.ids) and (ta.procedure_line_id.id) and (
                            ta.procedure_line_id.dependency_ids.ids):
                    activo = True
                    for de in ta.procedure_line_id.dependency_ids:
                        tarea_en_proyecto = self.env['project.task'].search(
                            [('id', 'in', todas.ids), ('procedure_line_id', '=', de.id)])
                        if (tarea_en_proyecto.stage_id.is_closed == False):
                            activo = False
                        ta['active'] = activo

            # Ahora las fechas límite:
            for ta in todas:
                diaobjetivo = 0
                if (ta.procedure_line_id.id) and (
                        ta.id not in exist.ids):  # <= Para permitir crear otras tareas manualmente, y mantener fechas límite si varios clicks
                    if ta.procedure_line_id.interval < 7:
                        diadelasemanahoy = datetime.date.today().strftime("%w")
                        diaobjetivo = int(diadelasemanahoy) + ta.procedure_line_id.interval
                        if diaobjetivo > 5:
                            interval = ta.procedure_line_id.interval + 2
                        else:
                            interval = ta.procedure_line_id.interval
                    else:
                        interval = ta.procedure_line_id.interval
                    fecha = datetime.datetime.today() + datetime.timedelta(days=interval)

                    ta['date_deadline'] = fecha.date()

            # Cambiar la etiqueta de las tareas en base a la plantilla:
            if record.procedure_id.task_name:
                record['label_tasks'] = record.procedure_id.task_name

