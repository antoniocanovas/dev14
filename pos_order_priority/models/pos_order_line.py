# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosOrderLine(models.Model):
	_inherit = 'pos.order.line'
	
	priority_id = fields.Many2one('pos.order.line.priority', string='Priority to delete')
	priority = fields.Char(string='Priority')
	priority_value = fields.Integer(string='Priority Value')
