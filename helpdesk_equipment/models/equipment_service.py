# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class EquipmentService(models.Model):
    _inherit = 'equipment.service'

    ticket_ids = fields.One2many('helpdesk.ticket','service_id')

    def _get_tickets(self):
        self.tickets_count = len(self.ticket_ids)
    tickets_count = fields.Integer('Tickets',compute=_get_tickets,store=False)
