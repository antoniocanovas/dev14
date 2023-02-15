from odoo import _, api, fields, models

TYPE = [
    ('ein', 'Employee expense billable'),
    ('eni', 'Internal employee expense'),
    ('pin', 'Product billable'),
    ('pni', 'Product not billable'),
    ('sin', 'Service billable'),
    ('sni', 'Service not billable'),
]

class ExternalWork(models.Model):
    _name = "external.work.line"
    _description = "External Work Line"


    name        = fields.Char(string='Name')
    type        = fields.Selection(selection=TYPE, string="Type", default=TYPE[0][0])

    date        = fields.Date(string='Date', related='external_work_id.date')
    employee_id = fields.Many2one('hr.employee', string="Employee")
    user_id     = fields.Many2one('res.users', string="User", related='employee_id.user_id')
    partner_id  = fields.Many2one('res.partner', string="Partner", related='external_work_id.partner_id')
    material_id = fields.Many2one('product.product', string='Material', domain="[('type','!=','service'),('sale_ok','=',True)]")
    service_id  = fields.Many2one('product.product', string='Service', domain="[('type','=','service'),('sale_ok','=',True)]")
    expense_id  = fields.Many2one('product.product', string='Expense', domain="[('can_be_expensed','=',True)]")

    @api.depends('type','material_id','service_id','expense_id')
    def get_product_id(self):
        product = self.material_id
        if self.type in ['ein','eni']: product = self.expense_id
        if self.type in ['sin','sni']: product = self.service_id
        self.product_id = product.id
    product_id  = fields.Many2one('product.product', string='Product', compute='get_product_id')

    product_qty = fields.Float('Qty')
    uom_id      = fields.Many2one('uom.uom', string='UOM', related='product_id.uom_id')

    ticket_amount = fields.Monetary('Ticket value', store=True, readonly=False)
    currency_id = fields.Many2one('res.currency', store=True, default=1)

    project_id  = fields.Many2one('project.project', string="Project", related='external_work_id.project_id')
    task_id     = fields.Many2one('project.task', string="Task")
    time_begin  = fields.Float('Begin')
    time_end    = fields.Float('End')

    hr_expense_id  = fields.Many2one('hr.expense', 'Expense line')
    analytic_line_id = fields.Many2one('account.analytic.line')
    sale_line_id = fields.Many2one('sale.order.line')
    sale_id = fields.Many2one('sale.order', string="Sale", related='external_work_id.sale_id')
    external_work_id = fields.Many2one('external.work', string='Work')
    work_type = fields.Selection('Work type', related='external_work_id.type')

    def get_create_timesheet_expense_sale(self):
        saleline, timesheet, expense = False, False, False
        if self.type in ['ein','eni','pin','pni','sin','sni']: saleline = True
        if self.type in ['ein','eni','pin','pni','sin','sni']: timesheet = True
        if self.type in ['ein','eni','pin','pni','sin','sni']: expense = True

        if (saleline == True):
            if not (self.external_work_id.sale_id.id):
                self.env['sale.order'].create({'partner_id':self.partner_id.id})