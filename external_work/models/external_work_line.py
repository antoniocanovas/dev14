from odoo import _, api, fields, models

TYPE = [
    ('ein', 'Employee expense to reinvoice'),
    ('eni', 'Internal employee expense'),
    ('pin', 'Product to invoice'),
    ('pni', 'Product not invoiced'),
    ('sin', 'Service to invoice'),
    ('sni', 'Service not invoiced or warranty')
]

class ExternalWork(models.Model):
    _name = "external.work.line"
    _description = "External Work Line"


    name        = fields.Char(string='Name')
    type        = fields.Selection(selection=TYPE, string="Type", default=TYPE[0][0])

    date        = fields.Date(string='Date')
    employee_id = fields.Many2one('hr.employee', string="Employee")
    user_id     = fields.Many2one('res.users', string="User", related='employee_id.user_id')
    partner_id  = fields.Many2one('res.partner', string="Partner", related='external_work_id.partner_id')
    product_id  = fields.Many2one('product.product', string='Product')
    product_qty = fields.Float('Qty')
    uom_id      = fields.Many2one('uom.uom', string='UOM')
    ticket_amount = fields.Monetary('Ticket value', store=True, readonly=False)
    currency_id = fields.Many2one('res.currency', store=True, default=1)

    task_id     = fields.Many2one('project.task', string="Task")
    project_id  = fields.Many2one('project.project', string="Project", related='task_id.project_id')
    time_begin  = fields.Float('Begin')
    time_end    = fields.Float('End')

    expense_id  = fields.Many2one('hr.expense', 'Expense')
    analytic_line_id = fields.Many2one('account.analytic.line')
    sale_line_id = fields.Many2one('sale.order.line')
    sale_id = fields.Many2one('sale.order', string="Sale")
    external_work_id = fields.Many2one('external.work', string='Work')

    def get_create_timesheet_expense_sale(self):
        saleline, timesheet, expense = False, False, False
        if self.type in ['ein','eni','pin','pni','sin','sni']: saleline = True
        if self.type in ['ein','eni','pin','pni','sin','sni']: timesheet = True
        if self.type in ['ein','eni','pin','pni','sin','sni']: expense = True

        if (saleline == True):
            if not (self.external_work_id.sale_id.id):
                self.env['sale.order'].create({'partner_id':self.partner_id.id})