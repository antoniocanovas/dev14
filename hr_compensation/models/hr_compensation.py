# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class HrCompensation(models.Model):
    _name = "hr.compensation"
    _description = "HR Employee time compensation"

    year = fields.Integer('Year', required=True, store=True)
    employee_id = fields.Many2one('hr.employee', required=True, store=True)

    anual_hour = fields.Integer('Anual hours')
