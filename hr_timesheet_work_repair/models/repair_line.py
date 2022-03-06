from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class RepairLine(models.Model):
    _inherit = 'repair.line'

    work_sheet_id = fields.Many2one('work.sheet')