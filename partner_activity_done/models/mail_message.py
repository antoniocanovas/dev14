from odoo import _, api, fields, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    name = fields.Char(string='Name', store=True)
    stage_id = fields.Many2one("mail.message.stage", "Stage")
    activity_type = fields.Char(string='Type', store=True)