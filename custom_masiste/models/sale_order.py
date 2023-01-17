# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    delegacion_id = fields.Many2one('res.partner', string='Delegación')
    contacto_id = fields.Many2one('res.partner', string='Contacto')
