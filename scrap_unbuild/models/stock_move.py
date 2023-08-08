# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = "stock.move"

    ## Versión que asigna subproductos a subproductos en caso de inventario (no ajuste):
    @api.depends('create_date')
    def get_unbuild_product_tmpl_id(self):
        for record in self:
            unbuild_product = False
            if (record.inventory_id.id):
                unbuild_product = record.inventory_id.unbuild_product_tmpl_id.id
            elif (not record.inventory_id.id) and (record.location_id.usage in ['inventory']):
                unbuild_product = record.product_id.product_tmpl_id.subparent_id.id
            record['unbuild_product_tmpl_id'] = unbuild_product
    unbuild_product_tmpl_id = fields.Many2one('product.template', string='Unbuild Parent', store=True, readonly=True,
                                              compute='get_unbuild_product_tmpl_id')



    ## Versión que pone siempre el vehículo principal, los subproductos no tienen hijos:
#    @api.depends('create_date')
#    def get_unbuild_product_tmpl_id(self):
#        if (self.inventory_id.id) or (self.location_id.usage == 'inventory'):
#            self.unbuild_product_tmpl_id = self.product_id.product_tmpl_id.parent_id.id
#    unbuild_product_tmpl_id = fields.Many2one('product.template', string='Unbuild Parent', store=True, readonly=True,
#                                                         compute='get_unbuild_product_tmpl_id')
