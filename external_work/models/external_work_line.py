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


    @api.depends('external_work_id','employee_id')
    def _get_workline_name(self):
        name=""
        if self.external_work_id.id: name += self.external_work_id.name
        if name: name += " - "
        if self.product_id.id: name += self.product_id.name
        self.name = name
    name = fields.Char('Name', compute='_get_workline_name', store=False)

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
    hr_expense_state = fields.Selection(related='hr_expense_id.state')
    analytic_line_id = fields.Many2one('account.analytic.line')
    sale_line_id = fields.Many2one('sale.order.line')
    sale_id = fields.Many2one('sale.order', string="Sale", related='external_work_id.sale_id')
    sale_state = fields.Selection(related='sale_id.state')
    external_work_id = fields.Many2one('external.work', string='Work')
    work_type = fields.Selection('Work type', related='external_work_id.type')

    # IDS lines so for record in self is required:
    @api.depends('sale_state','hr_expense_state')
    def _get_workline_is_readonly(self):
        for record in self:
            is_readonly = False
            if (record.hr_expense_state != 'draft') and (record.type in ['ein','eni']): is_readonly = True
            if (record.sale_state != 'draft') and (record.type in ['ein','pin','pni','sin']): is_readonly = True
            record['is_readonly'] = is_readonly
    is_readonly = fields.Boolean('Is readonly', compute='_get_workline_is_readonly', store=True, readonly=True)


