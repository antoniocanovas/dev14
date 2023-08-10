# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class UnbuildProductLineWizard(models.TransientModel):
    _name = "unbuild.product.line.wizard"
    _description = "Unbuild Product Line Wizard"

    unbuild_wizard_id = fields.Many2one('scrap.unbuild.wizard')
    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product template',
    )
    part_id = fields.Many2one(
        'unbuild.part',
        string='Part',
        required=True,
    )
    qty = fields.Integer(string='Quantity')

    @api.depends('part_id')
    def get_part_name(self):
        for record in self:
            record.name = record.part_id.name
    name = fields.Char(string='Name', compute='get_part_name', readonly=False, store=True)

    # Inventory valuation field:
    standard_price = fields.Float(string='Unit value')

    product_tmpl_categ_id = fields.Many2one('product.category', string='Category', related='product_tmpl_id.categ_id')
