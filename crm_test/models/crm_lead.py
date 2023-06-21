from odoo import _, api, fields, models


class CRMLead(models.Model):
    _inherit = 'crm.lead2opportunity.partner'

    action = fields.Selection([('exist', 'Exist'), ('nothing','Noting')])
