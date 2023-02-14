from odoo import _, api, fields, models

class ExternalWork(models.Model):
    _name = "external.work"
    _description = "External Work"
    _inherit = ['mail.thread', 'mail.activity.mixin']

TYPE = [
    ('sale', 'Sale'),
    ('project', 'Project'),
    ('task', 'Tasks'),
    ('warranty', 'Maintenance or warranty'),
]

    name        = fields.Char(string='Name')
    date        = fields.Date(string='Date')
    employee_id = fields.Many2one('hr.employee', string="Employee")
    user_id     = fields.Many2one('res.users', string="User", related='employee_id.user_id')
    project_id  = fields.Many2one('project.project', string="Project")
    task_id     = fields.Many2one('project.task', string="Task")
    sale_id     = fields.Many2one('sale.order', string="Sale")
    partner_id  = fields.Many2one('res.partner', string="Partner")
    sale_subtotal = fields.Float('Sale subtotal')
    sale_public =  fields.Float('Public price')
    signature   = fields.Binary('Signature')
    line_ids    = fields.One2many('external.work.line', string='Lines')
    company_id  = fields.Many2one('res.company')

#    @api.depends('unbuild_type')
#    def get_refurbish_is_outlet(self):
