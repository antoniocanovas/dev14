# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosNote(models.Model):
	_name = 'pos.note'
	_description = 'Pos Note'
	_rec_name = 'name'
	
	name = fields.Char('Name')