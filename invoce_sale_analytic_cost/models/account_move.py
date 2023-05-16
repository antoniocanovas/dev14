from odoo import api, fields, models, _

class AccountInvoice(models.Model):
    _inherit = 'account.move'


    def _create_analytic_line(self):
        if self.move_type in ['out_invoice']:
            for li in self.invoice_line_ids:
                if (li.analytic_account_id.id) and not (li.analytic_cost_id.id) \
                        and (li.product_id.product_tmpl_id.autoanalytic) and (self.state in ['posted']):
                    new = self.env['account.analytic.line'].create({
                        'name':li.product_id.name,
                        'account_id': li.analytic_account_id.id,
                        'product_id': li.product_id.id,
                        'unit_amount': li.quantity,
                        'product_uom_id': li.product_uom_id.id
                    })
                    #li['analytic_cost_id'] = new.id
