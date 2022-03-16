# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosOrderLinePriority(models.Model):
	_name = 'pos.order.line.priority'
	_description = 'Pos Order Line Priority'
	_rec_name = 'name'
	
	name = fields.Char('Name')
	value = fields.Integer('Value')
	color_code = fields.Char('Color Code', default="#2f4f4f")
