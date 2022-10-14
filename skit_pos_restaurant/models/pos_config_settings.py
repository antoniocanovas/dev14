# -*- coding: utf-8 -*-

# Import from odoo lib
from odoo import models, fields


class BaseModuleUninstall(models.TransientModel):
    _inherit = "base.module.uninstall"

    def action_uninstall(self):
        """this def is used to remove existing records in pos_sale_sync.sale_sync_field_ids in model ir_config_parameter,
            while uninstalling module."""

        self.env['ir.config_parameter'].search([('key', '=', 'pos_sale_sync.sale_sync_field_ids')]).unlink()
        res = super(BaseModuleUninstall, self).action_uninstall()
        return res

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_sync_field_ids = fields.Many2many('ir.model.fields', 'sale_sync_field_rel',
                                           string='Synchronized Fields',
                                           domain=[('model', 'in', ['sale.order', 'sale.order.line'])
                                                   ])

    def set_values(self):
        """ Add Fields in pos setting screen and set_values."""
        super(ResConfigSettings, self).set_values()
        config_parameters = self.env["ir.config_parameter"].sudo()
        for record in self:
            config_parameters.sudo().set_param("pos_sale_sync.sale_sync_field_ids", ', '.join(str(x) for x in record.sale_sync_field_ids.ids))
    
    def get_values(self):
        """ Get Fields to show the pos setting screen."""
        res = super(ResConfigSettings, self).get_values()
        config_parameters = self.env["ir.config_parameter"].sudo()
        sale_sync_field_ids = config_parameters.sudo().get_param("pos_sale_sync.sale_sync_field_ids", default=False)
        res.update(
            sale_sync_field_ids=sale_sync_field_ids and [(6,0, [int(x) for x in sale_sync_field_ids.split(',')])],
        )
        return res