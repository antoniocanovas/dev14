from odoo import _, api, fields, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.depends('create_date')
    def get_mail_message_name(self):
        for record in self:
            item_name = ""
            model_id = self.env['ir.model'].search([('model', '=', record.model)])
            item_id = self.env[record.model].search([('id', '=', record.res_id)])
            if item_id.id: item_name = item_id.name
            record['name'] = model_id.name + " => " + item_name
    name = fields.Char('Name', store=True, compute='get_mail_message_name')
