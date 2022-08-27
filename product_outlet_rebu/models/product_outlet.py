from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

TAX_TYPE = [
    ('rebu', 'REBU'),
    ('iva', 'IVA'),
]

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    outlet_estimation_ids = fields.One2many('product.outlet.estimation', 'product_outlet_id', string="Estimation")
    outlet_price = fields.Float(string="Price", store=True)
    outlet_tax_type = fields.Selection(selection=TAX_TYPE, string='Tax Type')

    @api.depends('outlet_estimation_ids')
    def get_total_estimations(self):
        for record in self:
            total = 0
            for line in record.outlet_estimation_ids:
                if not line.invoiced:
                    total += line.amount
            record.outlet_subtotal_estimation = total

    outlet_subtotal_estimation = fields.Float(string="Total estimation", store=False, compute="get_total_estimations")

    def get_total_analytic(self):
        for record in self:
            total = 0
            lines = self.env['account.analytic.line'].search([(
                'account_id', 'in', [record.income_analytic_account_id.id, record.expense_analytic_account_id.id])])

            for line in lines:
                if (line.product_id.product_tmpl_id.id == record.id) and (
                        line.move_id.move_id.move_type in ['out_invoice', 'out_refund']):
                    total += 0
                else:
                    total += line.amount
            record.outlet_subtotal_analytic = total
    outlet_subtotal_analytic = fields.Float(string="Total Analytic", store=False, compute="get_total_analytic")

    @api.depends('outlet_price', 'outlet_tax_type')
    def get_outlet_rebu_iva(self):
        for record in self:
            tax, rebu_amount = 0, 0
            if (record.outlet_tax_type == 'rebu'):
                analytic = self.env['account.analytic.line'].search(
                    [('account_id', '=', record.expense_analytic_account_id.id),
                     ('move_id.move_id.move_type', '=', 'in_invoice'),
                     ('product_id.product_tmpl_id', '=', record.id)])
                if analytic:
                    for li in analytic.ids:
                        rebu_amount += analytic.amount
                else:
                    for li in record.outlet_estimation_ids:
                        if (li.product_id.product_tmpl_id.id == record.id):
                            rebu_amount += li.amount
                if (record.outlet_price > -rebu_amount):
                    tax = (record.outlet_price + rebu_amount) * (1- 1/1.21)
            elif (record.outlet_tax_type != 'rebu'):
                tax = record.outlet_price * (1- 1/1.21)
            record.outlet_rebu_iva = -tax
    outlet_rebu_iva = fields.Float(string="REBU/IVA (€)", store=False, compute="get_outlet_rebu_iva")

    @api.depends('outlet_estimation_ids', 'outlet_price', 'outlet_tax_type')
    def get_outlet_margin(self):
        for record in self:
            price = record.outlet_price
            estimations = record.outlet_subtotal_estimation
            analytics = record.outlet_subtotal_analytic
            record.outlet_margin = price + estimations + analytics + record.outlet_rebu_iva
    outlet_margin = fields.Float(string="Margin (€)", store=False, compute="get_outlet_margin")

    def get_analytic_lines(self):
        for record in self:
            lines = self.env['account.analytic.line'].search([(
                'account_id', 'in', [record.income_analytic_account_id.id, record.expense_analytic_account_id.id])])
            record.analytic_line_ids = [(6, 0, lines.ids)]
    analytic_line_ids = fields.Many2many('account.analytic.line', store=False, readonly=True, string="Analytic",
                                         compute="get_analytic_lines")
