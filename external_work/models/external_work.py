from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


TYPE = [
    ('sale', 'Sale'),
    ('project', 'Project'),
    ('task', 'Tasks'),
    ('warranty', 'Maintenance or warranty'),
]

class ExternalWork(models.Model):
    _name = "external.work"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "External Work"

    type = fields.Selection(selection=TYPE, string="Type", default=TYPE[0][0])

    date        = fields.Date('Date')
    employee_id = fields.Many2one('hr.employee', string="Employee")
    user_id     = fields.Many2one('res.users', string="User", related='employee_id.user_id')
    project_id  = fields.Many2one('project.project', string="Project")
    task_id     = fields.Many2one('project.task', string="Task")
    sale_id     = fields.Many2one('sale.order', string="Sale")
    sale_state  = fields.Selection(related='sale_id.state')
    partner_id  = fields.Many2one('res.partner', string="Partner")
    sale_subtotal = fields.Monetary('Sale subtotal', related='sale_id.amount_untaxed')
    signed_by   = fields.Char('Signed by')
    signature   = fields.Binary('Signature')
    line_ids    = fields.One2many('external.work.line', 'external_work_id', string='Lines')
    company_id  = fields.Many2one('res.company')
    currency_id = fields.Many2one('res.currency', store=True, default=1)
    state = fields.Selection([('draft','Draft'),('done','Done')], store=True, default='draft')

    @api.depends('partner_id','employee_id')
    def _get_work_name(self):
        name=""
        if self.employee_id.id: name += self.employee_id.name
        if name: name += " - "
        if self.partner_id.id:  name += self.partner_id.name
        self.name = name
    name = fields.Char('Name', compute='_get_work_name', store=True)

    def action_work_confirm(self):
        # Create sale.order if not:
        if not self.sale_id.id:
            create_sale = False
            for li in self.line_ids:
                if li.type in ['ein', 'sin', 'pin', 'pno']: create_sale = True
            if create_sale == True:
                sale = self.env['sale.order'].create({'partner_id':self.partner_id.id})
                self.sale_id = sale.id

        for li in self.line_ids:
            timesheet, saleline, expense = False, False, False
            if li.type in ['ein','pin','pni','sin']: saleline = True
            if li.type in ['sin','sni']: timesheet = True
            if li.type in ['ein','eni']: expense = True
            if (saleline == True) and (li.sale_line_id.id == False):
                newsol = self.env['sale.order.line'].create({'product_id':li.product_id.id, 'name':li.product_id.name,
                                                             'product_uom':li.uom_id.id, 'product_uom_qty':li.product_qty,
                                                             'order_id':self.sale_id.id})
                li.sale_line_id = newsol.id

            if timesheet == True:
                newts = self.env['account.analytic.line'].create({'name':li.name, 'date':li.date,
                                                                  'task_id':li.task_id.id,
                                                                  'account_id':li.project_id.analytic_account_id.id,
                                                                  'unit_amount':li.product_qty, 'product_id':li.product_id.id,
                                                                  'employee_id':li.employee_id.id})
                li.analytic_line_id = newts.id

            if expense == True:
                newexpense = self.env['hr.expense'].create({'employee_id':li.employee_id.id, 'name': li.name,
                                                            'date': li.date, 'payment_mode':'own_account',
                                                            'unit_amount':li.ticket_amount / li.product_qty,
                                                            'product_id':li.product_id.id, 'quantity':li.product_qty,
                                                            'product_uom_id':li.uom_id.id,})
                li.hr_expense_id = newexpense.id

        self.state = 'done'


    def action_work_back2draft(self):
        # Check if possible, deleting timesheet, expense and salelines:
        if self.sale_state != 'draft':
            raise exceptions.ValidationError(
                _("Sale order state must be DRAFT to back this Work")
            )
        self.state = 'draft'

