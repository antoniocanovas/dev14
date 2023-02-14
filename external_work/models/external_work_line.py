from odoo import _, api, fields, models

class ExternalWork(models.Model):
    _name = "external.work"
    _description = "External Work"

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
    task_id     = fields.Many2one('project.task', string="Task")
    project_id  = fields.Many2one('project.project', string="Project", related='task_id.project_id')
    product_id  = fields.Many2one('product.product', string='Product')
    product_qty = fields.Float('Qty')
    uom_id      = fields.Many2one('uom.uom', string='UOM')
    ticket_value = fields.Monetary('Ticket value')
    time_begin  = fields.Float('Begin')
    time_end    = fields.Float('End')

    partner_id  = fields.Many2one('res.partner', string="Partner", related='external_work_id.partner_id')
    expense_id  = fields.Many2one('hr.expense', 'Expense')
    analytic_line_id = fields.Many2one('account.analytic.line')
    sale_line_id = fields.Many2one('sale.order.line')
    sale_id = fields.Many2one('sale.order', string="Sale")
    external_work_id = fields.Many2one('external.work', string='Work')

#    @api.depends('unbuild_type')
#    def get_refurbish_is_outlet(self):
