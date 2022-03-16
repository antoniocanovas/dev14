# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosNoteType(models.Model):
	_name = 'pos.note.type'
	_description = 'Pos Note Type'
	_rec_name = 'name'
	
	name = fields.Char('Name')
	note_ids = fields.Many2many('pos.note', 'pos_note_type_rel', 'note_id', 'type_id', 'Pos Note')