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
         ('subproduct', 'Subproducto'),
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
    stock_move_ids = fields.One2many('stock.move','unbuild_product_tmpl_id', string='Subproducts', store=True)

## PARA ELIMINAR:
    unbuild_set_id = fields.Many2one('unbuild.set', string='Unbuild Set')
    unbuild_product_line_ids = fields.One2many('unbuild.product.line', 'product_tmpl_id', string='Un.Prod Lines')

    def get_inventory_line_ids(self):
### MODIFICAR PARA: a) buscar productos por código desguazados, b) todos los SI de estos, c) todos los SIL de SIs
### Considerar sólo los directos para subproductos, y todos para el principal tal como hace get_unbuild_subproducts.
        si_ids = self.env['stock.inventory'].search([('unbuild_product_tmpl_id', '=', self.id)])
        sil_ids = self.env['stock.inventory.line'].search([('inventory_id', 'in', si_ids.ids)])
        sil = []
        for li in sil_ids:
            if li.product_qty != li.theoretical_qty:
                sil.append(li.id)
        self.inventory_line_ids = [(6, 0, sil)]
    inventory_line_ids = fields.Many2many('stock.inventory.line', compute='get_inventory_line_ids', store=False)

## Sustituirá a las líneas de inventario (el anterior):
# Pendiente asignar el unbuild_product_tmpl_id al inventario que se hace a mano ... ????
    def get_stock_move_ids(self):
        si_ids = self.env['stock.inventory'].search([('unbuild_product_tmpl_id', '=', self.id)])
        sm_ids = self.env['stock.move'].search([('inventory_id', 'in', si_ids.ids)])
        self.unbuild_sm_ids = [(6,0,sm_ids.ids)]
    unbuild_sm_ids = fields.Many2many('stock.move', compute='get_stock_move_ids', store=False)



## Pendiente eliminar cuando tengamos ok las sil o los sm anteriores:
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