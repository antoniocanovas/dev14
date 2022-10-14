# -*- coding: utf-8 -*-
# imports of odoo lib
from odoo import models, fields


class res_users(models.Model):
    _inherit = "res.users"

    pos_config_id = fields.Many2one("pos.config",
                                    string="POS Configuration")
