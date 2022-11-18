# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    donation_set_id = fields.Many2one('donation.set', string='Donation Set')
    donation_line_ids = fields.One2many('donation.line', 'purchase_id', string='Donation Lines')

    # Crea las líneas de compra con nuevos productos seriados por el código de compra:
    def create_purchase_order_line_from_donation_lines(self):
        for r in records:
            for li in r.donation_line_ids:
                donation_code = r.name
                if not li.purchase_line_id.id:
                    similar_product = env['purchase.order.line'].search(
                        [('product_id.parent_id', '=', li.product_id.product_tmpl_id.id), ('order_id', '=', record.id)])
                    if similar_product.ids:
                        donation_code += "_" + str(len(similar_product))

                    new_product = env['product.template'].create(
                        {'name': li.name + " " + donation_code, 'categ_id': li.product_id.categ_id.id,
                         'sale_ok': True, 'purchase_ok': True, 'type': 'product',
                         'parent_id': li.product_id.product_tmpl_id.id})

                    new_productproduct = env['product.product'].search([('product_tmpl_id', '=', new_product.id)])

                    new_pol = env['purchase.order.line'].create(
                        {'order_id': record.id, 'product_id': new_productproduct.id, 'product_qty': li.qty,
                         'product_uom': li.product_id.uom_po_id.id, 'price_unit': 1})

                    li.write({'newproduct_id': new_product.id, 'purchase_line_id': new_pol.id})


    # Actualizar líneas de donaciones, al cambiar el SET:
    @api.depends('donation_set_id')
    def update_donation_set_lines(self):
        self.donation_line_ids.unlink()
        for line in self.donation_set_id.line_ids:
            newline = self.env['donation.line'].create({'product_id': line.product_id.id,
                                                        'qty': line.qty,
                                                        'name': line.product_id.name,
                                                        'purchase_id': record.id})
