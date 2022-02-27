from odoo import _, api, fields, models
from datetime import datetime, timezone, timedelta
import pytz
import base64
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class TimesheetWorkSheet(models.Model):
    _name = 'timesheet.work.sheet'

    type = fields.Selection(selection_add=[('repair','Repair')], related='work_id.type')
    repair_id = fields.Many2one('repair.order', string="Repair Order")
    repair_location_id = fields.Many2one('stock.location', related='repair_id.location_id', string='Origin Location')

    repair_product_ids = fields.One2many('repair.line', 'work_sheet_id', string='Parts')

    @api.depends('work_id')
    def get_repairs(self):
        for record in self:
            repairs = []
            partner = record.work_id.partner_id
            if (partner.id) and (record.type == 'repair'):
                repairs = self.env['repair.order'].search([('partner_id', '=', partner.id), ('state', 'not in', ['draft', 'done', 'cancel'])]).ids
            elif (not partner.id) and (record.type == 'repair'):
                repairs = self.env['repair.order'].search([('state', 'not in', ['draft', 'done', 'cancel'])]).ids
            record.repair_ids = [(6, 0, repairs)]

    repair_ids = fields.Many2many('repair.order', compute=get_repairs, store=False)

#    @api.depends('project_service_ids', 'project_product_ids', 'repair_service_ids', 'repair_product_ids','mrp_service_ids', 'mrp_product_ids')
#    def get_workread_only(self):
#        for record in self:
#            isreadonly = False
#            if record.project_service_ids or record.project_product_ids or record.repair_service_ids.ids or record.repair_product_ids or record.mrp_service_ids or record.mrp_product_ids:
#                isreadonly = True
#            record['work_readonly'] = isreadonly
#    work_readonly = fields.Boolean(string='Read only', compute=get_workread_only, store=True)

