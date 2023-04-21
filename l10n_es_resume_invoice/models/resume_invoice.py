# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class ResumeInvoice(models.Model):
    _name = 'resume.invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Resume Invoice'

    name = fields.Char(string='Nombre', required=True)
    date = fields.Date(string='Fecha')
    partner_id = fields.Many2one('res.partner', string='Fecha')
    pos_order_ids = fields.One2many('pos.order', 'resume_invoice_id', string='Tickets')


    @api.depends('create_date')
    def _get_pos_resume_invoice_code(self):
        self.name = self.env['ir.sequence'].next_by_code('pos.resume.invoice.code')
    name = fields.Char('Code', store=True, readonly=True, compute=_get_pos_resume_invoice_code)
