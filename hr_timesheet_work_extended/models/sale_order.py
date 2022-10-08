from odoo import _, api, fields, models

import logging

_logger = logging.getLogger(__name__)


class SaleOrderiSet(models.Model):
    _inherit = 'sale.order'

#   Eliminado Antonio 8/10:
#    work_id = fields.Many2one('timesheet.work', 'Work')
