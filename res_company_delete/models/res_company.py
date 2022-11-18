# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
from time import sleep
from datetime import datetime, timedelta
import json
from random import randint
import requests
import img2pdf
from PIL import Image
import io
from odoo import fields, models, api
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'


    def company_save_delete(self):
        for r in self:
            pickings = self.env['stock.picking'].search([('company_id', '=', r.id)])
            for pi in pickings:
                for sm in pi.move_ids_without_package:
                    for sml in sm.move_line_ids:
                        sml['state'] = 'draft'
                        sml.unlink()
                    sm['state'] = 'draft'
                    sm.unlink()
                pi['state'] = 'draft'
                pi.unlink()

            saleorders = self.env['sale.order'].search([('company_id', '=', r.id)])
            for so in saleorders:
                so['state'] = 'draft'
                so.unlink()

            invoices = self.env['account.move'].search(
                [('move_type', 'in', ['out_invoice', 'in_invoice', 'out_refund', 'in_refund']),
                 ('company_id', '=', 'r.id')])
            for fa in invoices:
                fa.button_draft()
                fa.button_cancel()
            for fa in invoices:
                fa.unlink()

            purchaseorders = self.env['purchase.order'].search([('company_id', '=', r.id)])
            for po in purchaseorders:
                po.button_cancel()
                po['state'] = 'cancel'
                po.unlink()

            fiscalposition = self.env['account.fiscal.position'].search([('company_id', '=', r.id)])
            for fp in fiscalposition: fp.unlink()

            journals = self.env['account.journal'].search([('company_id', '=', r.id)])
            for jo in journals: jo.unlink()

            taxs = self.env['account.tax'].search([('company_id', '=', r.id)])
            for tax in fiscalposition: tax.unlink()

            accounts = self.env['account.account'].search([('company_id', '=', r.id)])
            for aa in accounts: aa.unlink()

            config = self.env['res.config.settings'].search([('company_id', '=', r.id)])
            config.write({'chart_template_id': False, 'sale_tax_id': False, 'purchase_tax_id': False})

        # r.unlink()




