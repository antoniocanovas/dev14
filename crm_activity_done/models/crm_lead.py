from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    mail_activity_done = fields.One2many('mail.message', 'lead_id', store=True)
