from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = 'project.project'

    @api.depends('sale_order_id')
    def get_work_id(self):
        if not self.work_id:
            self.work_id = self.sale_order_id.work_id

    work_id = fields.Many2one('work.work', 'Work extended', compute='get_work_id', readonly=False)