# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class UnbuildSet(models.Model):
    _name = "unbuild.set"
    _description = "Set for unbuilds"

    name = fields.Char(string='Name')
    line_ids = fields.One2many(
        'unbuild.set.line',
        'set_id',
        string='Part',
    )
