# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    unbuild_type = fields.Selection(
        [('main', 'Vehículo o Parte para desguace'),
         ('subproduct', 'Subproducto (desguazable si tiene asignado un Vehículo o Parte PADRE)'),
         ('refurbish','Para compra/venta'),
         ('other','Otros finales desguazados')],
        string='Scrap Type')

    parent_id = fields.Many2one(
        'product.template',
        string='Vehicle',
        domain=[('unbuild_type', '=', 'main')],
    )
    unbuild_location_id = fields.Many2one(
        'stock.location',
        string='Parts location',
    )
    unbuild_project_id = fields.Many2one(
        'project.project',
        string='Project',
    )
    unbuild_task_id = fields.Many2one(
        'project.task',
        string='Parts task',
    )

    unbuild_sequence = fields.Integer(string='Sequencia de piezas')

    unbuild_set_id = fields.Many2one('unbuild.set', string='Unbuild Set')

    unbuild_product_line_ids = fields.One2many('unbuild.product.line', 'product_tmpl_id', string='Un.Prod Lines')

    @api.depends('unbuild_product_line_ids')
    def get_unbuild_subproducts(self):
        for record in self:
            subproducts = []
            if record.unbuild_type == 'main':
                subproducts = self.env['product.template'].search([('parent_id','=',record.id)]).ids
            elif record.unbuild_type == 'subproduct':
                for li in record.unbuild_product_line_ids:
                    if li.newproduct_id.id:
                        subproducts.append(li.newproduct_id.id)
            record.subproduct_ids = [(6,0,subproducts)]
    subproduct_ids = fields.Many2many('product.template', string='Subproductos',
                                      store=False, compute=get_unbuild_subproducts)

    @api.depends('unbuild_type','name','default_code')
    def compute_unbuild_type_readonly(self):
        for record in self:
            ro = False
            if (record.name == False): ro = True
            if (record.default_code != False) and (record.unbuild_type != False): ro = True
            record['unbuild_type_readonly'] = ro
    unbuild_type_readonly = fields.Boolean('Readonly context', store=True, compute=compute_unbuild_type_readonly)