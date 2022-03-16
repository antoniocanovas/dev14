# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    priority_ids = fields.Many2many('pos.order.line.priority', 'restaurant_order_priority_rel', 'order_id', 'priority_id', 'Priority')
