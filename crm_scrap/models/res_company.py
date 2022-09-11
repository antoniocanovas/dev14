# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


import logging

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    scrap_warehouse_project_id = fields.Many2one('project.project', string='Warehouse Project')
    scrap_warehouse_user_id = fields.Many2one('res.users', string='Warehouse Default User')

