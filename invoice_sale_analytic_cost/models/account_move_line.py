from odoo import fields, models, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    analytic_cost_id = fields.Many2one('account.analytic.line', string='Analytic cost', store=True)
