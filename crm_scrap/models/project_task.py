from odoo import _, api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    lead_id = fields.Many2one('crm.lead', string="Lead", store=True)
    brand_id = fields.Many2one('product.brand', string="Brand")
    categ_id = fields.Many2one('scrap.category', string="Category")
    product_id = fields.Many2one('product.product', string="Producto")
    crm_stage_type = fields.Selection(related='lead_id.stage_id.type', store=True)
    
    @api.depends('crm_stage_type')
    def get_int_value_to_paint_tree_colors(self):
        for record in self:
            value = 0
            if record.crm_stage_type == 'comercial': value=1
            if record.crm_stage_type == 'taller': value=2
            if record.crm_stage_type == 'administracion': value = 3
            record['crm_stage_integer'] = value
    crm_stage_integer = fields.Integer('Code for colors', store=False, compute='get_int_value_to_paint_tree_colors')

    @api.depends('partner_id')
    def _get_partner_tags(self):
        for record in self:
            tags = []
            if (record.partner_id.parent_id.id) and (record.partner_id.parent_id.category_id.ids):
                for tag in record.partner_id.parent_id.category_id: tags.append(tag.id)
            if (record.partner_id.category_id.ids):
                for tag in record.partner_id.category_id: tags.append(tag.id)
            record['partner_tag_ids'] = [(6,0,tags)]
    partner_tag_ids = fields.Many2many('res.partner.category', compute='_get_partner_tags', store=False, string='Partner Tags')