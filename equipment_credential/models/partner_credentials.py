# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class PartnerCredentialEquipment(models.Model):
    _inherit = 'partner.credentials'

    equipment_id = fields.Many2one('maintenance.equipment', string="Equipment")


