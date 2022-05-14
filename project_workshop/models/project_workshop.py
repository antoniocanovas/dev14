# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _
from datetime import datetime
from odoo.tools import html2plaintext

class ProjectWorkshop(models.Model):
    _name = "project.workshop"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Workshop Services (from Projects)"

    name = fields.Char('Asunto', required=True, store=True)
    description = fields.Html('Notas')
    solution = fields.Text('Solución')
    project_id = fields.Many2one('project.project', string='Proyecto')
    project_partner_id = fields.Many2one('res.partner', related='project_id.partner_id', string='Cliente', store=True)
    is_new = fields.Boolean("Nuevo")
    pre_offer = fields.Boolean("Presupuestar antes")
    warranty = fields.Boolean("En garantía")
    license = fields.Char('Matrícula')
    partner_id = fields.Many2one('res.partner', 'Cliente')
    model = fields.Char('Marca y modelo')
    user_id = fields.Many2one('res.users', string='Técnico')
    sale_line_id = fields.Many2one('sale.order.line', string='Línea de pedido')
    sale_id = fields.Many2one('sale.order', related='sale_line_id.order_id', string='Presupuesto')
    task_id = fields.Many2one('project.task', string='Tarea')
    stage_id = fields.Many2one('project.task.type', string='Etapa', related='task_id.stage_id', store=True)
    date_in = fields.Date('Entrada', default=lambda self: datetime.today())
    date_deadline = fields.Date('Compromiso')
    date_out = fields.Date('Entregado')
    estimated_time = fields.Float('Horas estimadas')
    estimated_product = fields.Monetary('Estimación material')
    effective_hours = fields.Float('Horas imputadas', related='task_id.effective_hours')
    active = fields.Boolean('Activo', default=True)
    currency_id = fields.Many2one('res.currency', default=1)

    @api.depends('description')
    def get_test(self):
        for record in self:
            record['test'] = html2plaintext(record.description)
    test = fields.Text('test', compute='get_test')

    company_id = fields.Many2one("res.company", "Compañía",
        default=lambda self: self.env.company, ondelete="cascade")

    @api.depends('stage_id', 'date_out')
    def _get_is_closed(self):
        for record in self:
            closed = False
            if (record.stage_id.is_closed == True) and (record.date_out != False):
                closed = True
            record.is_closed = closed
    is_closed = fields.Boolean('Cerrado', compute='_get_is_closed', store=True)

    def action_set_date_out(self):
        for record in self:
            record.date_out=datetime.now()

    def action_view_project(self):
        self.ensure_one()
        action_window = {
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            "name": "Project Project",
            "views": [[False, "form"]],
            "context": {"create": False, "show_project": True},
            "res_id": self.project_id.id
        }
        return action_window

    def action_view_task(self):
        self.ensure_one()
        action_window = {
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "name": "Project Task",
            "views": [[False, "form"]],
            "context": {"create": False, "show_task": True},
            "res_id": self.task_id.id
        }
        return action_window

    def action_view_so(self):
        self.ensure_one()
        action_window = {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "name": "Sale Order",
            "views": [[False, "form"]],
            "context": {"create": False, "show_order": True},
            "res_id": self.sale_id.id
        }
        return action_window

    def create_workshop_task(self):
        for record in self:
            project, kanban_state = record.project_id, 'normal'

            # Tarea bloqueada inicialmente si el cliente requiere presupuesto:
            if record.pre_offer == True:
                kanban_state = 'blocked'

            if (record.is_new == True) and (record.project_id.id == False):
                # Crear Proyecto:
                name = "[" + record.license + "] " + record.model
                project = self.env['project.project'].create(
                    {'name': name, 'partner_id': record.partner_id.id, 'allow_timesheets': True,
                     'allow_billable': True, })
                record.write({'project_id': project.id, 'is_new': False})

            # Crear pedido de venta con línea de servicio y tarea asociada a la línea:
            if (record.sale_line_id.id == False) and (record.warranty == False):
                saleorder = self.env['sale.order'].create({'partner_id': project.partner_id.id})
                saleline = self.env['sale.order.line'].create(
                    {'order_id': saleorder.id, 'product_id': project.timesheet_product_id.id})
                record['sale_line_id'] = saleline.id
                name = record.name
                if record.pre_offer == True:
                    name += " **"
                task = self.env['project.task'].create({'name': name, 'project_id': project.id,
                    'description': record.description, 'partner_id': project.partner_id.id,
                    'date_deadline':record.date_deadline, 'planned_hours':record.estimated_time,
                    'sale_line_id': saleline.id, 'kanban_state': kanban_state})
            if (record.warranty == True):
                task = self.env['project.task'].create({'name': record.name, 'project_id': project.id,
                    'description': record.description, 'partner_id': project.partner_id.id,
                    'date_deadline':record.date_deadline, 'planned_hours':record.estimated_time})
            if task.id:
                record['task_id'] = task.id
