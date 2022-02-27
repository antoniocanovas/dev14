from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


TYPES = [
    ('project', 'Project'),
]


class IsetsTypes(models.Model):
    _name = 'timesheet.work'
    _description = 'Timesheet Work'

    name = fields.Char('Name', required=True)
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    type = fields.Selection([('project', 'Project')], required=True, string='Type', default='project')
    project_id = fields.Many2one('project.project')
    set_start_stop = fields.Boolean('Set start & stop time')

