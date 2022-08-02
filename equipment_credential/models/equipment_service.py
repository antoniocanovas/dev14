# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class EquipmentService(models.Model):
    _name = 'equipment.service'
    _description = 'Equipment Service'

    name = fields.Char('Name')
    type_id = fields.Many2one('equipment.service.type', string="Type")


