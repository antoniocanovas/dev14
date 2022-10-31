# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Serincloud SL
##############################################################################
from odoo import api, fields, models, _


class WorkPickingWizard(models.Model):
    _name = "work.picking.wizard"
    _description = "Work Sheet Picking Wizard"
    _transient = True

    work_sheet_id = fields.Many2one('work.sheet', string='Sheet', store=True)
    picking_ids = fields.Many2many('stock.picking', related='work_sheet_id.order_picking_ids')
