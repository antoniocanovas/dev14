# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class UnbuildSetLine(models.Model):
    _name = "unbuild.set.line"
    _description = "Line for unbuilds"


    part_id = fields.Many2one(
        'unbuild.part',
        string='Part',
    )
    set_id = fields.Many2one(
        'unbuild.set',
        string='Set',
    )
    qty = fields.Integer(string='Quantity')

    def get_set_name(self):
        for record in self:
            record['name'] = str(record.qty) + 'x' + record.part_id.name
    name = fields.Char(string='Name', store=True, compute='get_set_name')
