from odoo import _, api, fields, models

import logging

_logger = logging.getLogger(__name__)


class SaleOrderiSet(models.Model):
    _inherit = 'sale.order'

    iset_consumed_ids = fields.One2many('account.analytic.line', 'sale_id', string='Work Sheet')
    new_sale_id = fields.Many2one('sale.order', string='New quotation')
