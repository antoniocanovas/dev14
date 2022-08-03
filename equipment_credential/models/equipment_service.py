# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class EquipmentService(models.Model):
    _inherit = 'equipment.service'

    credential_ids = fields.One2many('partner.credentials', 'service_id')

    def _get_credentials_service(self):
        results = self.env['partner.credentials'].search([('service_id', '=', self.id)])
        self.credential_count = len(results)
    credential_count = fields.Integer('Credentials', compute=_get_credentials_service, store=False)


