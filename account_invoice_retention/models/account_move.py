# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Antonio Cánovas & PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class AccountMove(models.Model):
    _name = 'account.move'

    retention_enable = fields.Boolean('Retention', default=False)
    retention_description = fields.Char('Description')
    retention_type = fields.Selection([('fixed_net', 'Fixed net'),
                                       ('fixed_gross', 'Fixed gross'),
                                       ('percent_net', 'Percent net'),
                                       ('percent_gross', 'Percent Gross')], string='Type')
    retention_percent = fields.Float('Percent')

