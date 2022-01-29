from odoo import fields, models, api


class PosCategoryMulti(models.Model):
    _inherit = "product.template"


    pos_additional_categ_ids  = fields.Many2many(
        'pos.category',
        'pos_product_category_rel','pos_category_id','product_tmpl_id',
        string='Additional Categories')
    pos_category_ids = fields.Many2many(
        'pos.category',
        'pos_product_category_add_rel','pos_category_id','product_tmpl_id',
        string="POS Categories",
        help="Those categories are used to group similar products for point of sale.",
        compute='compute_pos_category_ids',store=True
    )

    @api.depends('categ_id','pos_additional_categ_ids')
    def compute_pos_category_ids(self):
        for record in self:
            categories = []
            if record.pos_categ_id.id:
                categories.append(record.pos_categ_id.id)
            for ca in record.pos_additional_categ_ids:
                categories.append(ca.id)
        record['pos_category_ids'] = [(6, 0, categories)]
    #            pos_categ_ids = []
    #            pos_categ_ids = product.pos_categ_id.ids if product.pos_categ_id else self.env['pos.category']
    #            pos_categ_ids += product.pos_additional_categ_ids.ids if product.pos_additional_categ_ids else []
    #            product.pos_category_ids = pos_categ_ids
