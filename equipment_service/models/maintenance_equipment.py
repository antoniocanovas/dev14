# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class MaintenanceEquipmentCredentials(models.Model):
    _inherit = 'maintenance.equipment'

    ip_address = fields.Char('Ip Address')
    pathway_id = fields.Many2one('equipment.service', name="Pathway",
                                 domain=[('type_id.is_pathway','=',True)])
    service_ids = fields.One2many('equipment.service', 'equipment_id')

    def _get_services_equipment(self):
        results = self.env['equipment.service'].search([('equipment_id', '=', self.id)])
        self.services_count = len(results)
    services_count = fields.Integer('Credentials', compute=_get_services_equipment, store=False)
