# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectProcedure(models.Model):
    _name = 'project.procedure.gap'
    _description = 'Etapas en procedimiento de proyectos'

    name = fields.Char(string='Nombre', required=True)
    priority = fields.Integer(string='Prioridad')
    user_id = fields.Many2one('res.users', string='Responsable', required=True, store=True)
    date_limit = fields.Date(string='Fecha límite')
    project_id = fields.Many2one('project.project', string='Proyecto')

    state = fields.Selection([('new', 'Nuevo'), ('working', 'En curso'), ('done', 'Terminado'),
                              ('cancel', 'Cancelado')], default='new', string='Estado')
    type = fields.Selection([('lead','Oportunidad'), ('sale','Venta'), ('purchase','Compra'), ('task','Tarea'),
                             ('picking','Albarán'),('invoice','Factura')], required=True)

    lead_id = fields.Many2one('crm.lead', string='Oportunidad')
    sale_id = fields.Many2one('sale.order', string='Venta')
    purchase_id = fields.Many2one('purchase.order', string='Compra')
    task_id = fields.Many2one('project.task', string='Tarea')
    picking_id = fields.Many2one('stock.picking', string='Albarán')
    invoice_id = fields.Many2one('account.move', string='Factura')
