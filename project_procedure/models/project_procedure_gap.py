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

    lead_ids = fields.Many2many('crm.lead')
    sale_ids = fields.Many2many(comodel_name='sale.order',
                                relation='project_gap_rel',
                                column1='gap_id',
                                column2='sale_id',
                                ))
    purchase_ids = fields.Many2many('purchase.order')
    task_ids = fields.Many2many('project.task')
    picking_ids = fields.Many2many('stock.picking')
    invoice_ids = fields.Many2many('account.move')
