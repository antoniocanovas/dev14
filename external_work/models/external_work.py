from odoo import _, api, fields, models

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

    date = fields.Date('Date')
    employee_id = fields.Many2one('hr.employee', string="Employee")
    user_id     = fields.Many2one('res.users', string="User", related='employee_id.user_id')
    project_id  = fields.Many2one('project.project', string="Project")
    task_id     = fields.Many2one('project.task', string="Task")
    sale_id     = fields.Many2one('sale.order', string="Sale")
    partner_id  = fields.Many2one('res.partner', string="Partner")
    sale_subtotal = fields.Float('Sale subtotal')
    sale_public =  fields.Float('Public price')
    signed_by   = fields.Char('Signed by')
    signature   = fields.Binary('Signature')
    line_ids    = fields.One2many('external.work.line', 'external_work_id', string='Lines')
    company_id  = fields.Many2one('res.company')
    currency_id = fields.Many2one('res.currency', store=True, default=1)
    state = fields.Selection([('draft','Draft'),('done','Done')], store=True, default='draft')

    @api.depends('partner_id','employee_id','type')
    def _get_work_name(self):
        name=""
        if self.employee_id: name += self.employee_id.name
        if name: name += " - "
        if self.partner_id:     name += self.partner_id.name
        self.name = name
    name = fields.Char('Name', compute='_get_work_name')

    def action_work_confirm(self):
        self.state = 'done'

    def action_work_back2draft(self):
        self.state = 'draft'

    def get_create_timesheet_expense_sale(self):
        saleline, timesheet, expense = False, False, False
        if self.type in ['ein','eni','pin','pni','sin','sni']: saleline = True
        if self.type in ['ein','eni','pin','pni','sin','sni']: timesheet = True
        if self.type in ['ein','eni','pin','pni','sin','sni']: expense = True

        if (saleline == True):
            if not (self.external_work_id.sale_id.id):
                self.env['sale.order'].create({'partner_id':self.partner_id.id})
