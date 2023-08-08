# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    dictionary_name = fields.Many2one('product.dictionary', store=True, copy=True)
    uses = fields.Text('Product Uses')
    references = fields.Text('References')
    ref_market = fields.Char(
        string='Ref. visible',
        help='La referencia que tiene escrita o troquelada la pieza.'
    )
    ref_oem = fields.Char(
        string='Ref. OEM',
        help='La referencia del fabricante del tractor.'
    )

    @api.onchange('dictionary_name')
    def copy_dictionary_name(self):
        self.name = self.dictionary_name.name

    @api.depends('seller_ids.product_code')
    def get_ref_supplier_codes(self):
        name = ""
        for li in self.seller_ids:
            if li.product_code:
                name += li.product_code + " "
        self.ref_supplier = name
    ref_supplier = fields.Char('Supplier codes', compute='get_ref_supplier_codes', store=True, readonly=True)

    barcode = fields.Char(compute='_get_barcode', store=True)

    @api.depends('ref_market', 'ref_oem')
    def _get_quant_refs(self):
        for record in self:
            product_list, quants = [], []
            if (record.ref_market != False):
                products = self.env['product.product'].search([('ref_market', '=', record.ref_market)])
                product_list.extend(products.ids)
            if (record.ref_oem != False):
                products = self.env['product.product'].search([('ref_oem', '=', record.ref_oem)])
                product_list.extend(products.ids)
            if len(product_list) != 0:
                quants = self.env['stock.quant'].search(
                    [('product_id', 'in', products.ids), ('location_id.usage', '=', 'internal')]).ids
            record['quant_refs'] = [(6, 0, quants)]
    quant_refs = fields.Many2many('stock.quant', store=False, compute='_get_quant_refs')


    @api.depends('default_code')
    def _get_barcode(self):
        for record in self:
            if record.default_code and not record.barcode:
                print("DEBUG2", record.barcode)
                record.barcode = record.default_code

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100,
                     name_get_uid=None):
        res = super()._name_search(
            name, args=args, operator=operator, limit=limit,
            name_get_uid=name_get_uid)
        if name:
            tmpl_product_ids = self._search(
                ['|', '|', '|', '|', '|',
                ('uses', operator, name),
                ('chassis_pt', operator, name),
                ('ref_oem', operator, name),
                ('ref_market', operator, name),
                ('references', operator, name),
                ('description', operator, name)], limit=limit,
                access_rights_uid=name_get_uid)
            print(tmpl_product_ids)
            for tmpl in tmpl_product_ids:
                res.append(tmpl.id)
        return res

    @api.depends('qty_available')
    def _get_stock_global_pt(self):
        for record in self:
            stock_global_pt = 0
            quants = record.env['stock.quant'].sudo().search([('product_tmpl_id','=',record.id),('location_id.usage','=','internal')])
            for qu in quants: stock_global_pt += qu.quantity
            record['stock_global_pt'] = stock_global_pt
    stock_global_pt = fields.Float('Stock Global', store=False, compute='_get_stock_global_pt')

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.depends('seller_ids.product_code')
    def get_ref_supplier_codes(self):
        name = ""
        for li in self.seller_ids:
            if li.product_code:
                name += li.product_code + " "
        self.ref_supplier = name
    ref_supplier = fields.Char('Supplier codes', compute='get_ref_supplier_codes', store=True, readonly=True)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100,
                     name_get_uid=None):
        res = super()._name_search(
            name, args=args, operator=operator, limit=limit,
            name_get_uid=name_get_uid)
        if name:
            product_ids = self.env['product.product'].search(
                 ['|', '|', '|', '|', '|',
                 ('uses', operator, name),
                 ('chassis_pp', operator, name),
                 ('ref_oem', operator, name),
                 ('ref_market', operator, name),
                 ('references', operator, name),
                 ('description', operator, name)],
                  limit=limit)
            for tmpl in product_ids:
                res.append(tmpl.id)
        return res

    @api.depends('qty_available')
    def _get_stock_global_pp(self):
        for record in self:
            stock_global = 0
            quants = record.env['stock.quant'].sudo().search([('product_id','=',record.id),('location_id.usage','=','internal')])
            for qu in quants: stock_global += qu.quantity
            record['stock_global_pp'] = stock_global
    stock_global_pp = fields.Float('Stock total', store=False, compute='_get_stock_global_pp')
