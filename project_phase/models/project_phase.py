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
            if (record.type == 'lead') and (record.lead_id.id):
                state = 'Flujo de venta'
                if (record.lead_id.probability == 0):
                    state = 'Perdido'
                elif (record.lead_id.probability == 100):
                    state = 'Ganado'
            elif (record.type == 'sale') and (record.sale_id.id):
                state = record.sale_id.state
            elif (record.type == 'purchase') and (record.purchase_id.id):
                state = record.purchase_id.state
            elif (record.type == 'task') and (record.task_id.id):
                state = record.task_id.stage_id.name
            elif (record.type == 'picking') and (record.picking_id.id):
                state = record.picking_id.state
            elif (record.type == 'invoice') and (record.invoice_id.id) and (record.invoice_id.state != 'posted'):
                state = record.invoice_id.state
            elif (record.type == 'invoice') and (record.invoice_id.id) and (record.invoice_id.state == 'posted'):
                state = record.invoice_id.payment_state
            record.state = state
    state = fields.Char(string='Estado', compute="_get_phase_state", store=True, default='New')
