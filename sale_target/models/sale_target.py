# Copyright Serincloud
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models, api

import logging
_logger = logging.getLogger(__name__)



class SaleTarget(models.Model):
    _name = 'sale.target'
    _description = 'Sale Target'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    user_id = fields.Many2one('res.users', string='User')
    currency_id = fields.Many2one('res.currency', default=1)
    team_id = fields.Many2one('crm.team', related='user_id.sale_team_id', string='Team')
    invoiced_amount = fields.Monetary(string='Invoiced')
    target = fields.Monetary(string='Target')
    lead_count = fields.Integer(string='Leads', readonly=True)
    lead_amount = fields.Monetary(string='Leads amount', readonly=True)

    sale_over_target = fields.Monetary('Sale over Target', related='target', store=False)
    gap_vs_lead = fields.Monetary('Gap vs leads', related='target_gap', store=False)
    gap_vs_quotation = fields.Monetary('Gap vs quotations', related='target_gap', store=False)
    lead_vs_gap = fields.Monetary('Leads vs Gap', related='lead_amount', store=False)
    quotation_vs_gap = fields.Monetary('Quotations vs Gap', related='quotation_amount', store=False)

    sale_count = fields.Integer(string='Sales', readonly=True)
    sale_margin = fields.Monetary(string='Sales margin', readonly=True)
    sale_amount = fields.Monetary(string='Sales amount', readonly=True)
    quotation_count = fields.Integer(string='Quotations', readonly=True)
    quotation_margin = fields.Monetary(string='Quotations margin', readonly=True)
    quotation_amount = fields.Monetary(string='Quotations amount', readonly=True)
    quarter_ids = fields.One2many('sale.target.quarter', 'target_id', string="Quarters")
    target_year = fields.Integer('Year')
    lead_lt_gap = fields.Boolean('Leads < GAP')
    quotation_lt_gap = fields.Boolean('Quotations < GAP')
    target_lt_sale = fields.Boolean('Sale over target')

    @api.depends('target','sale_amount')
    def get_target_gap(self):
        for record in self:
            record['target_gap'] = record.target - record.sale_amount
    target_gap = fields.Monetary(string='Target GAP', compute='get_target_gap', store=False)

    @api.depends('target','sale_amount')
    def get_target_multiple(self):
        for record in self:
            multiple = int(record.sale_amount / record.target) +1
            record['target_multiple'] = record.target * multiple
    target_multiple = fields.Monetary(string='Target Multiple', compute='get_target_multiple', store=False)
