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
            state = 'Pendiente'
            if (type == 'lead') and (lead_id.id):
                state = 'Flujo de venta'
                if (lead_id.probability == 0):
                    state = 'Perdido'
                elif (lead_id.probability == 100):
                    state = 'Ganado'
            elif (type == 'sale') and (sale_id.id):
                state = sale_id.state
            elif (type == 'purchase') and (purchase_id.id):
                state = purchase_id.state
            elif (type == 'task') and (task_id.id):
                state = task_id.stage_id.name
            elif (type == 'picking') and (picking_id.id):
                state = picking_id.state
            elif (type == 'invoice') and (invoice_id.id) and (invoice_id.state != 'posted'):
                state = invoice_id.state
            elif (type == 'invoice') and (invoice_id.id) and (invoice_id.state == 'posted'):
                state = invoice_id.payment_state
            record.state = state
    state = fields.Char(string='Estado', compute="_get_phase_state", store=True, default='New')
