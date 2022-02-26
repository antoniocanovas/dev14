from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    partner_id = fields.Many2one('res.partner', related='sale_id.partner_id')

    @api.depends('origin')
    def get_sale_id(self):
        for record in self:
            so = self.env['sale.order'].search([('name', '=', record.origin)])
            record['sale_id'] = so.id
    sale_id = fields.Many2one('sale.order', compute=get_sale_id)
