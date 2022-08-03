# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class EquipmentService(models.Model):
    _name = 'equipment.service'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Equipment Service'

    name = fields.Char('Name')
    type_id = fields.Many2one('equipment.service.type', string="Type")
    equipment_id = fields.Many2one('maintenance.equipment', string="Equipment")
    note = fields.Text('Description')
    active = fields.Boolean('Active', default=True)

