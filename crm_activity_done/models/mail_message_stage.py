# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class MailMessageMStage(models.Model):
    _name = "mail.message.stage"
    _description = "Mail message stage"

    name = fields.Char(string='Name')
    sequence = fields.Integer(string="Sequence")
