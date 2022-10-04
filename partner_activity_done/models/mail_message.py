from odoo import _, api, fields, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.depends('create_date')
    def get_mail_message_name(self):
        for record in self:
            model_name, item_name = "", "", ""
            model_id = self.env['ir.model'].search([('model', '=', record.model)])
            item_id = self.env[record.model].search([('id', '=', record.res_id)])
            if model_id.id: model_name = item_id.name
            if item_id.id: item_name = item_id.name
            if model_id.id or item_id.id: name = model_name + " => " + item_name
            record['name'] = name
    name = fields.Char('Name', compute='get_mail_message_name', store=True)
