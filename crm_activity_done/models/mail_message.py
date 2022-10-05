from odoo import _, api, fields, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.depends('create_date')
    def get_mail_message_fields(self):
        for record in self:
            name, stage_name = "", ""
            model_id = self.env['ir.model'].search([('model', '=', record.model)])
            item_id = self.env[record.model].search([('id', '=', record.res_id)])

            if (model_id.name): name = model_id.name
            if (item_id.stage_id.id): stage_name = item_id.stage_id.name
            stage_id = self.env['mail.message.stage'].search([('name','=',stage_name)])
            if not stage_id.id: stage_id = self.env['mail.message.stage'].create({'name':stage_name})

            line = record.body.split("\n")[2]
            line = line.split("<span>")[1]
            line = line.split("</span>")[0]

            record.write({'name': name, 'stage_id': stage_id.id, 'activity_type': line})
