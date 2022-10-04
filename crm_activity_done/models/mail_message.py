from odoo import _, api, fields, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.depends('create_date')
    def get_mail_message_name(self):
        for record in self:
            model_id = self.env['ir.model'].search([('model', '=', record.model)])
            item_id = self.env[model].search([('id', '=', record.res_id)])
            record['name'] = model_id.name + " => " + item_id.name
    name = fields.Char('Name', compute='get_mail_message_name')

    @api.depends('create_date')
    def get_activity_lead(self):
        for record in self:
            lead = False
            if (record.model == 'crm.lead') and \
                    (record.message_type == 'notification') \
                    and (record.subtype_id.id == 3):
                lead = self.env['crm.lead'].search([('id', '=', record.res_id)]).id
            record['lead_id'] = lead
    lead_id = fields.Many2one('crm.lead', string="Lead", store=True, compute='get_activity_lead')
