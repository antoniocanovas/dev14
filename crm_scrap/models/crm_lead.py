from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    task_ids = fields.One2many('project.task', 'lead_id', store=True)
    scrap_project_id = fields.Many2one('project.project', store=False, related='company_id.scrap_project_id')
    scrap_user_id = fields.Many2one('res.users', store=False, related='company_id.scrap_user_id')
