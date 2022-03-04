from odoo import _, api, fields, models

import logging

_logger = logging.getLogger(__name__)


class SaleOrderiSet(models.Model):
    _inherit = 'sale.order'

    def get_worksheets_products(self):
        for record in self:
            aal = []
            if record.analytic_account_id.id:
                aal = self.env['account.analytic.line'].search([
                    ('account_id','=',record.analytic_account_id.id),
                    ('product_id.type','in',['product','consu'])]).ids
            record.product_consumed_ids = [(6, 0, aal)]
    product_consumed_ids = fields.Many2many('account.analytic.line', compute=get_worksheets_products, store=False)
    new_sale_id = fields.Many2one('sale.order', string='New quotation')
