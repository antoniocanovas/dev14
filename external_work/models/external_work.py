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

name = fields.Char('Name')
type = fields.Selection(selection=TYPE, string="Type", default=STATES[0][0])

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
line_ids    = fields.One2many('external.work.line', string='Lines')
company_id  = fields.Many2one('res.company')
