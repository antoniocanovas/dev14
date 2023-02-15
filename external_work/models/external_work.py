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
    signature   = fields.Binary('Signature')
    line_ids    = fields.One2many('external.work.line', 'external_work_id', string='Lines')
    company_id  = fields.Many2one('res.company')
    currency_id = fields.Many2one('res.currency', store=True, default=1)

    @api.depends('partner_id','employee_id','type')
    def _get_work_name(self):
        name=""
        if self.employee_id: name += self.employee_id.name + " - "
        if self.type:           name += self.type[1] + " - "
        if self.partner_id:     name += self.partner_id.name
        self.name = name
    name = fields.Char('Name', compute='_get_work_name')
