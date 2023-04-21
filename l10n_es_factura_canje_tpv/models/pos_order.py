from odoo import _, api, fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    resume_invoice_id = fields.Many2many(comodel_name='resume.invoice',
                                         relation='posorder_canje_rel',
                                         column1='resume_invoice_id',
                                         column2='posorder_id',
                                         string="Factura de canje",
                                         )
