# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectPhase(models.Model):
    _name = 'project.phase'
    _description = 'Project phases'

    name = fields.Char(string='Nombre', required=True)
    priority = fields.Integer(string='Prioridad')
    user_id = fields.Many2one('res.users', string='Responsable', required=True, store=True)
    date_limit = fields.Date(string='Fecha límite')
    project_id = fields.Many2one('project.project', string='Proyecto')
    type = fields.Selection([('lead','Oportunidad'), ('sale','Venta'), ('purchase','Compra'), ('task','Tarea'),
                             ('picking','Albarán'),('invoice','Factura')], required=True)

    lead_id = fields.Many2one('crm.lead', string='Oportunidad')
    sale_id = fields.Many2one('sale.order', string='Venta')
    purchase_id = fields.Many2one('purchase.order', string='Compra')
    task_id = fields.Many2one('project.task', string='Tarea')
    picking_id = fields.Many2one('stock.picking', string='Albarán')
    invoice_id = fields.Many2one('account.move', string='Factura')

    @api.depends('write_date')
    def _get_phase_state(self):
        for record in self:
            record.state = 'hola'
    state = fields.Char(string='Estado', compute="_get_phase_state", store=True)
    #[('new', 'Nuevo'), ('working', 'En curso'), ('done', 'Terminado'), ('cancel', 'Cancelado')], default='new',
