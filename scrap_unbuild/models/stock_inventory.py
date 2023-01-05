# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    unbuild_product_tmpl_id = fields.Many2one(
        'product.template',
        string='Unbuild Product',
    )

    # STOCK VALUE decreasing when unbuild:
    @api.depends('state')
    def update_unbuild_parent_product_value(self):
        if (self.product_tmpl_id.id) and (self.state == 'done'):
            stock_value = self.product_tmpl_id.standard_price - li.qty * li.standard_price
            if stock_value < 0: stock_value = 0
            self.product_tmpl_id.write({'standard_price':stock_value})
