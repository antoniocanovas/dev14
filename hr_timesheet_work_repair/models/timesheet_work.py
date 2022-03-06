from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

class TimesheetWork(models.Model):
    _inherit = 'timesheet.work'


    type = fields.Selection(selection_add=[('repair','Repair'),('project',)], ondelete={'repair': 'set default'})

