from odoo import _, api, fields, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.depends('create_date')
    def get_mail_message_name(self):
        for record in self:
            name = ""
            if (record.subtype_id == 3) and (record.message_type == 'notification'):
                model_id = self.env['ir.model'].search([('model', '=', record.model)])
                item_id = self.env[record.model].search([('id', '=', record.res_id)])
                if (model_id.name != ""): name += model_id.name
                if (model_id.name != "" and item_id.name != ""): name += " => "
                if (item_id.name != "" and item_id.name != ""): name += item_id.name
            record['name'] = name
    name = fields.Char(string='Name', compute='get_mail_message_name', store=False)
