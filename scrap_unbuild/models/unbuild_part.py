# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class UnbuildPart(models.Model):
    _name = "unbuild.part"
    _description = "Parts of scrap product"

    name = fields.Char(string='Name')
    category_id = fields.Many2one(
        'product.category',
        string='Category',
        required=True,
    )
