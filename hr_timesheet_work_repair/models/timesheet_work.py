from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

class TimesheetWork(models.Model):
    _name = 'timesheet.work'
    _description = 'Timesheet Work'

    type = fields.Selection(selection_add=[('repair','Repair')], ondelete={'repair': 'set null'})

