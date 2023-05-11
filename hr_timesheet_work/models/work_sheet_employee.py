from odoo import _, api, fields, models
from datetime import datetime, timezone, timedelta
import pytz
import base64
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class WorkSheetEmployee(models.Model):
    _name = 'work.sheet.employee'
    _description = 'Work Sheet Employee time'

    employee_id = fields.Many2one('hr.employee', store=True, readonly=True)
    work_id = fields.Many2one('timesheet.work')
    amount = fields.Float('Hours', store=True, readonly=True)
