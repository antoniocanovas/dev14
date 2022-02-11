# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

import logging

_logger = logging.getLogger(__name__)


class AccountInvoiceSuasor(models.Model):
    _inherit = 'account.move'

    suasor_invoice_id = fields.Many2one('suasor.invoice', 'Suasor')