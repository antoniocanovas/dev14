# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models

class HrEmployee(models.Model):
	_inherit = 'hr.employee'

	pricelist_ids = fields.Many2many('product.pricelist', string="Pricelists")