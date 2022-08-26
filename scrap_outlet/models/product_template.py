from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

VEHICLE_STATE = [
    ('used', 'Usado'),
    ('new', 'Nuevo'),
    ('km0', 'Kilómetro 0'),
    ('refurbish', 'Reparado'),
]

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    outlet_use = fields.Integer(string='Hours / Km')
    outlet_date = fields.Date(string="Date")
    outlet_model_id = fields.Many2one("fleet.vehicle.model", string="Model")
    outlet_brand_id = fields.Many2one("fleet.vehicle.model.brand",
                                       related="vehicle_model_id.brand_id",
                                       string="Brand")
    outlet_category_id = fields.Many2one("fleet.vehicle.category", string="Category")

    outlet_state = fields.Selection(selection=VEHICLE_STATE, string="Estado")
    outlet_license = fields.Char('Matrícula')

    @api.depends('unbuild_type')
    def get_refurbish_is_outlet(self):
        for record in self:
            outlet = record.outlet
            if (record.unbuild_type == 'refurbish'):
                outlet = True
            record.outlet = outlet
