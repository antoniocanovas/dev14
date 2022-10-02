# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class DonationSetLine(models.Model):
    _name = "donation.set.line"
    _description = "Donation lines"

    item_id = fields.Many2one(
        'product.product',
        string='Item',
    )
    set_id = fields.Many2one(
        'donation.set',
        string='Set',
    )
    qty = fields.Integer(string='Quantity')

    def get_set_name(self):
        for record in self:
            record['name'] = str(record.qty) + 'x' + record.item_id.name
    name = fields.Char(string='Name', store=True, compute='get_set_name')
