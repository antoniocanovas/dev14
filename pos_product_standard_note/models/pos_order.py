# -*- coding: utf-8 -*-

from odoo import fields, models, api, _ , tools


class PosOrderLine(models.Model):
	_inherit = 'pos.order.line'
	
	order_note = fields.Char('Order Notes')