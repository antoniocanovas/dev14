from odoo import _, api, fields, models
from datetime import datetime, timezone, timedelta
import pytz
import base64
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class WorkSheetTask(models.Model):
    _name = 'work.sheet.task'
    _description = 'Work Sheet Task time'

    name = fields.Char('Name')
    task_id = fields.Many2one('project.task', store=True, readonly=True)
    work_id = fields.Many2one('timesheet.work')
    amount = fields.Float('Hours', store=True, readonly=True)
