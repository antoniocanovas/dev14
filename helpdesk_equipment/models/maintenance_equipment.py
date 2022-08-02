# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    ticket_ids = fields.One2many('helpdesk.ticket','equipment_id')

    def _get_tickets(self):
        self.tickets_count = len(self.ticket_ids)

    tickets_count = fields.Integer('Tickets',compute=_get_tickets,store=False)

    def action_view_equipment_tickets(self):
        action = self.env.ref(
            'helpdesk_equipment.action_view_equipment_tickets').read()[0]
        return action

