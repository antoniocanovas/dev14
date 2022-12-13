# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class UnbuildProductLine(models.Model):
    _name = "unbuild.product.line"
    _description = "Unbuild Product Line"

    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product template',
    )
    part_id = fields.Many2one(
        'unbuild.part',
        string='Part',
        required=True,
    )
    newproduct_id = fields.Many2one(
        'product.template',
        string='New product',
    )
    qty = fields.Integer(string='Quantity')

    @api.depends('part_id')
    def get_part_name(self):
        for record in self:
            record.name = record.part_id.name
    name = fields.Char(string='Name', compute='get_part_name', readonly=False, store=True)

    # Inventory valuation field:
    standard_price = fields.Float(string='Unit stock value')
