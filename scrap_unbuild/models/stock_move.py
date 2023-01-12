# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends('create_date')
    def get_unbuild_product_tmpl_id(self):
        if self.inventory_id.id:
            self.unbuild_product_tmpl_id = self.product_id.product_tmpl_id.parent_id.id
    unbuild_product_tmpl_id = fields.Many2one('product.template', string='Unbuild Parent', store=True, readonly=True,
                                                         compute='get_unbuild_product_tmpl_id'
                                              )
