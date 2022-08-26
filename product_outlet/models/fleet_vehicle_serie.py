from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class FleetVehicleSerie(models.Model):
    _name = 'fleet.vehicle.serie'
    _description = 'Serial number for vehicles'

    name = fields.Char(string='Name')
    model_id = fields.Many2one("fleet.vehicle.model", string="Model")
    brand_id = fields.Many2one("fleet.vehicle.model.brand",
                                       related="model_id.brand_id",
                                       string="Brand")
    date_in = fields.Date(string='Date in')
    date_out = fields.Date(string='Date out')
