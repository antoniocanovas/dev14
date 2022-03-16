# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
	_inherit = 'product.template'
	
	pos_note_type_id = fields.Many2one('pos.note.type', 'Pos Note Type')