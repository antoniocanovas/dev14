from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    task_ids = fields.One2many('project.task',
                               related='lead_id',
                               store=True)

    @api.depends('create_date')
    def get_lead_self(self):
        for record in self:
            lead = self.env['crm.lead'].search([('id', '=', record.id)])
            record.self = lead.id
    self = fields.Many2one('crm.lead', string="Self", store=True, compute="get_lead_self")

