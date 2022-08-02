# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class PartnerCredentialEquipment(models.Model):
    _inherit = 'partner.credentials'

    service_id = fields.Many2one('equipment.service', string="Service")
    equipment_id = fields.Many2one('maintenance.equipment', string="Equipment", related='service_id.equipment_id')


