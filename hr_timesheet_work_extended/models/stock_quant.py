from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    work_id = fields.Many2one('work.work', related='location_id.work_id')