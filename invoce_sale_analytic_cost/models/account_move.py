from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class AccountInvoice(models.Model):
    _inherit = "account.move"


    def _create_analytic_line(self):
        if self.move_type in ['out_invoice']:

            for li in record.invoice_line_ids:
                if not (li.analytic_cost_id.id) and (li.analytic_account_id.id) and \
                        (li.product_id.product_tmpl_id.autoanalytic) and (self.state in ['posted']):

                    if li.product_uom_id.uom_type == 'reference':
                        cost = li.product_id.standard_price
                    elif li.product_uom_id.uom_type == 'bigger':
                        cost = li.product_id.standard_price * li.product_uom_id.factor_inv
                    elif li.product_uom_id.uom_type == 'smaller':
                        cost = li.product_id.standard_price / li.product_uom_id.factor
                    cost = - cost * li.quantity

                    new = self.env['account.analytic.line'].create({
                        'name':li.product_id.name,
                        'account_id': li.analytic_account_id.id,
                        'product_id': li.product_id.id,
                        'unit_amount': li.quantity,
                        'product_uom_id': li.product_uom_id.id,
                        'amount': cost
                    })
                    li['analytic_cost_id'] = new.id
        else:
            raise ValidationError('Opción válida para facturas de venta confirmadas.')