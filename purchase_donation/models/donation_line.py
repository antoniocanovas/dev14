# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class DonationLine(models.Model):
    _name = "donation.line"
    _description = "Donation Line"

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
    )
    qty = fields.Integer(string='Quantity')
    purchase_id = fields.Many2one('purchase.order', store=True, string='Purchase')

    newproduct_id = fields.Many2one(
        'product.template',
        string='New product',
    )

    @api.depends('product_id')
    def get_part_name(self):
        for record in self:
            record.name = record.product_id.name
    name = fields.Char(string='Name', compute='get_part_name', readonly=False, store=True)


