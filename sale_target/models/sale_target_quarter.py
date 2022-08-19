# Copyright Serincloud
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models, api

import logging
_logger = logging.getLogger(__name__)



class SaleTargetQuarter(models.Model):
    _name = 'sale.target.quarter'
    _description = 'Sale Target Quarter'

    name = fields.Char(string='Name', required=True)
    currency_id = fields.Many2one('res.currency', default='1')
    target_id = fields.Many2one('sale.target', 'string'='Target')
    lead_count = fields.Integer(string='Leads', readonly=True)
    lead_amount = fields.Monetary(string='Leads amount', readonly=True)
    sale_count = fields.Integer(string='Sales', readonly=True)
    sale_amount = fields.Monetary(string='Sales amount', readonly=True)
    quotation_count = fields.Integer(string='Quotations', readonly=True)
    revision_count = fields.Monetary(string='Quotations margin', readonly=True)
    quarter_id = fields.Many2one('sale.target', string="Quarter")
