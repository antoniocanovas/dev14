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
    sale_count = fields.Integer(string='Sales', readonly=True)
    sale_margin = fields.Monetary(string='Sales margin', readonly=True)
    sale_amount = fields.Monetary(string='Sales amount', readonly=True)
    quotation_count = fields.Integer(string='Quotations', readonly=True)
    quotation_margin = fields.Monetary(string='Quotations margin', readonly=True)
    quotation_amount = fields.Monetary(string='Quotations amount', readonly=True)
    quarter_ids = fields.One2many('sale.target.quarter', 'target_id', string="Quarters")
    target_year = fields.Integer('Year')

    @api.depends('target','sale_amount')
    def get_target_pending(self):
        for record in self:
            record['target_pending'] = record.target - record.sale_amount
    target_pending = fields.Monetary(string='Pending Target', compute='get_target_pending', store=False)

