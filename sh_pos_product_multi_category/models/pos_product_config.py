# Copyright (C) Softhealer Technologies.
# Part of Softhealer Technologies.

from odoo import models, fields


class PosProductConfig(models.Model):
    _inherit = 'product.template'

    sh_pos_categ_ids = fields.Many2many(
        'pos.category', string='Extra Pos Category', domain="[('id', '!=', pos_categ_id)]")
