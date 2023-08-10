from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    brand_id = fields.Many2one('product.brand', string="Brand")
    task_ids = fields.One2many('project.task', 'lead_id', store=True)
    scrap_project_id = fields.Many2one('project.project', store=False, related='company_id.scrap_project_id')
    scrap_user_id = fields.Many2one('res.users', store=False, related='company_id.scrap_user_id')
    market_value    = fields.Monetary('Market value', currency_field='company_currency')
    quotation_value = fields.Monetary('Quotation', currency_field='company_currency')
    description_tech = fields.Text('Technical notes', store=True)
    partner_ref = fields.Char('Cód. cliente', store=True, related='partner_id.ref')

    # Lo quito porque lo pide Cristina 9/8/23, siempre seleccionarán empresa y sólo se muestran etiquetas del primer contacto:
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
#    partner_tag_ids = fields.Many2many('res.partner.category', related='partner_id.category_id', readonly=False, store=True, string='Partner Tags')

    @api.depends('partner_id')
    def _get_partner_ref(self):
        for record in self:
            ref = ""
            if (record.partner_id.parent_id.id) and (record.partner_id.parent_id.ref):
                ref = record.partner_id.parent_id.ref
            else:
                ref = record.partner_id.ref
            record['partner_ref'] = ref
    partner_ref = fields.Char('Ref', compute='_get_partner_ref')
