# -*- coding: utf-8 -*-

# imports of odoo lib
from odoo import api, fields, models, _


class PosCategory(models.Model):
    _inherit = "pos.category"
    
    self_served = fields.Boolean(string='Self Served', default=False)
