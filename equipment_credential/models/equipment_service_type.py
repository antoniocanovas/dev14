# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class EquipmentServiceType(models.Model):
    _name = 'equipment.service.type'
    _description = 'Equipment Service Type'

    name = fields.Char('Name')
    is_pathway = fields.Boolean("Is pathway")
