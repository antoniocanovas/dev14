# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "res.company"

    unbuild_location_id = fields.Many2one(
        'stock.location',
        string='Unbuild location',
        domain=[('usage','=','internal')],
    )
    refurbish_location_id = fields.Many2one(
        'stock.location',
        string='Refurbish location',
        domain=[('usage','=','internal')],
    )
    unbuild_manager_id = fields.Many2one(
        'res.users',
        string='Unbuild Manager',
    )
