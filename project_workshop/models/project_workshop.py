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

    name = fields.Char('Asunto')
    note = fields.Text('Notas')
    project_id = fields.Many2one('project.project', string='Vehículo')
    project_partner_id = fields.Many2one('res.partner', related='project_id.partner_id', string='Cliente')
    is_new = fields.Boolean("Nuevo")
    license = fields.Char('Matrícula')
    partner_id = fields.Many2one('res.partner', 'Cliente')
    model = fields.Char('Marca y modelo')
    user_id = fields.Many2one('res.user', string='Técnico')

    #api.depends('')
    #def create_work_shop(self):
    #    for record in self:
