from odoo import fields, models, api

class ProductCategRel(models.Model):
    _name = 'pos.product.category.rel'
    _description = 'Pos categories rel'

    pos_category_id = fields.Many2one(
       'pos.category'
    )
    product_tmpl_id = fields.Many2one(
        'product.template'
    )


class ProductCategAddRel(models.Model):
    _name = 'pos.product.category.add.rel'
    _description = 'Pos categories add rel'

    pos_category_id = fields.Many2one(
       'pos.category'
    )
    product_tmpl_id = fields.Many2one(
        'product.template'
    )

