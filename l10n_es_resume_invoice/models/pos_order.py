from odoo import _, api, fields, models


class MailMessage(models.Model):
    _inherit = 'pos.order'

    resume_invoice_id = fields.Many2one('resume.invoice', string="Resume Invoice")
