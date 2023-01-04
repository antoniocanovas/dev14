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
    product_tmpl_id = fields.Many2one('product.template',string='Product',
                                      help='Si asignas un producto, al despiezar se añadirá la cantidad al stock.'
                                           'Se utilizarán sus fotos y precio de este producto sin distinción con otras piezas similares.')
