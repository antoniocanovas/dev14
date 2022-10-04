from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    activity_done_ids = fields.One2many('mail.message', 'author_id', store=True,
                                        domain=[('subtype_id','=',3),('message_type','=','notification')])

    #def _compute_activity_done_count(self):
    #    results = self.env['mail.activity'].search([('partner_id', '=', self.id)])
    #    self.activity_done_count = len(results)

    activity_done_count = fields.Integer(string="'Activity's", store=False)