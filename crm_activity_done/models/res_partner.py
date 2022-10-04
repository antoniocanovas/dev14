from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    activity_done_ids = fields.One2many('mail.message', 'author_id', store=True)
