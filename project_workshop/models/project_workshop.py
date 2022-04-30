# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class ProjectWorkshop(models.Model):
    _name = "project.workshop"
    _description = ""

    name = fields.Char('Asunto', required=True, store=True)
    description = fields.Html('Notas')
    project_id = fields.Many2one('project.project', string='Proyecto')
    project_partner_id = fields.Many2one('res.partner', related='project_id.partner_id', string='Cliente')
    is_new = fields.Boolean("Nuevo")
    warranty = fields.Boolean("En garantía")
    license = fields.Char('Matrícula')
    partner_id = fields.Many2one('res.partner', 'Cliente')
    model = fields.Char('Marca y modelo')
    user_id = fields.Many2one('res.users', string='Técnico')
    sale_line_id = fields.Many2one('sale.order.line', string='Línea de pedido')
    sale_id = fields.Many2one('sale.order', related='sale_line_id.order_id', string='Presupuesto')
    task_id = fields.Many2one('project.task', string='Tarea')
    stage_id = fields.Many2one('project.task.type', string='Etapa', related='task_id.stage_id')
    is_closed = fields.Boolean('Cerrado', related='stage_id.is_closed')
    date_in = fields.Date('Entrada')
    date_deadline = fields.Date('Compromiso')
    date_out = fields.Date('Entregado')
    active = fields.Boolean('Activo', default=True)

    def create_workshop_task(self):
        for record in self:
            project = record.project_id
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
                task = self.env['project.task'].create(
                    {'project_id': project.id, 'name': record.name, 'description': record.description,
                     'partner_id': project.partner_id.id, 'sale_line_id': saleline.id})
            if (record.warranty == True):
                task = self.env['project.task'].create(
                    {'project_id': project.id, 'name': record.name, 'description': record.description,
                     'partner_id': project.partner_id.id})
            if task.id:
                record['task_id'] = task.id
