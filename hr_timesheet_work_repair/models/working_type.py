from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class WorkingType(models.Model):
    _name = 'working.type'
    _description = 'Types of jobs/works'

    name = fields.Char('Name')
    extra_time = fields.Boolean('Extra')