from odoo import _, api, fields, models


class Lead2opportunity(models.TransientModel):
#    _inherit = 'crm.lead2opportunity.partner'
    _inherit = 'crm.lead2opportunity.partner.mass.action'
    action = fields.Selection(selection='_get_types', string='Related Customer',
                              compute='_compute_action', readonly=False, store=True, compute_sudo=False)

    @api.model
    def _get_types(self):
        selection = [
#            ('create', 'Create a new customer'),
            ('exist', 'Link to an existing customer'),
            ('nothing', 'Do not link to a customer')
        ]
        return selection
