# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Serincloud
##############################################################################
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    phone2 = fields.Char('Phone 2', store=True)
    ref = fields.Char('Cód. cliente')
