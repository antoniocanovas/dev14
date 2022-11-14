# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    roadmap_count = fields.Integer('Roadmaps', compute="_compute_roadmap_count", store=False)
    def _compute_roadmap_count(self):
        for record in self:
            total = 0
            roadmaps = self.env['project.roadmap'].search([('sale_id', '=', record.id),('active','in',[True,False])])
            if roadmaps.ids: total = len(roadmaps.ids)
        record['roadmap_count'] = total


