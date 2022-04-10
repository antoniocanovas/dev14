# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models

class HrEmployee(models.Model):
	_inherit = 'hr.employee'

	floors_ids = fields.Many2many('restaurant.floor', string="POS Floors")
	
