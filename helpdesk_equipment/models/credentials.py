# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class PartnerCredentialsHelpdesk(models.Model):
    _inherit = 'partner.credentials'

    ticket_ids = fields.One2many('helpdesk.ticket','partner_credentials_id')

    def _get_tickets(self):
        self.tickets_count = len(self.ticket_ids)

    tickets_count = fields.Integer('Tickets',compute=_get_tickets,store=False)

    def action_view_tickets(self):
        action = self.env.ref(
            'partner_credentials_helpdesk.action_view_tickets').read()[0]
        return action

