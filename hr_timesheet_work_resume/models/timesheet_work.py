from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

class TimesheetWork(models.Model):
    _name = 'timesheet.work'

