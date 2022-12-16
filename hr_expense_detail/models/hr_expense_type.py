from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class HrExpenseType(models.Model):
    _name = 'hr.expense.type'
    _description = 'Expense Type'

    name = fields.Char('Name', required=True)
#    product_id = fields.Many2one('product.template', domain="[('can_be_expensed','=',True)])")
    active = fields.Boolean('Active', default=True)
    amount = fields.Float('Standard Amount', required=True)