# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = "account.move"

    def get_sale_attachment(self):
        for record in self:
            sales = []
            for aml in record.invoice_line_ids:
                for li in aml.sale_line_ids:
                    if li.order_id.id not in sales:
                        sales.append(li.order_id.id)
            data = self.env['ir.attachment'].search([('res_model', '=', 'sale.order'), ('res_id', 'in', sales)])
            record.sale_attachment_ids = [(6, 0, data.ids)]
    sale_attachment_ids = fields.Many2many(comodel_name='ir.attachment',
                                           relation='account_sale_attachment_rel',
                                           column1='account_move_id',
                                           column2='attachment_id',
                                           store=False,
                                           compute='get_sale_attachment',
                                           string='Archivos')
