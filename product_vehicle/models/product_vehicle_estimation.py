from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProductVehicleEstimation(models.Model):
    _name = 'product.vehicle.estimation'
    _description = 'Vehicle Estimations'

    product_vehicle_id = fields.Many2one('product.template', string="Vehicle")
    product_id = fields.Many2one('product.product', string="Related Product", required=True)
    amount = fields.Float(string='Amount')
    invoiced = fields.Boolean("Invoiced")
    date = fields.Date(string='Date')

