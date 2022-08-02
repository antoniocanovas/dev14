# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class MaintenanceEquipmentCredentials(models.Model):
    _inherit = 'maintenance.equipment'

    credentials_ids = fields.One2many('partner.credentials', 'equipment_id')

    def _get_credentials_equipment(self):
        results = self.env['partner.credentials'].search([('equipment_id', '=', self.id)])
        self.credential_count = len(results)
    credential_count = fields.Integer('Credentials', compute=_get_credentials_equipment, store=False)
