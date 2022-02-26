from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


TYPES = [
    ('project', 'Project'),
    ('repair', 'Repair'),
    ('production', 'Production'),
]


class IsetsTypes(models.Model):
    _name = 'work.work'
    _description = 'iSet Work'

    name = fields.Char('Name', required=True)
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    repair_service_id = fields.Many2one('product.product', string='Product', domain=[('type', '=', 'service')])
    type = fields.Selection(selection=TYPES, required=True, string='Type')
    production_sale_id = fields.Many2one('sale.order')
    project_id = fields.Many2one('project.project')
    production_loss_id = fields.Many2one('mrp.workcenter.productivity.loss', string='Loss')
    set_start_stop = fields.Boolean('Set start & stop time')

