from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    activity_done_ids = fields.One2many('mail.message', 'author_id', store=True,
                                        domain=[('subtype_id','=',3),('message_type','=','notification')])
