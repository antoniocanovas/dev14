import logging
_logger = logging.getLogger(__name__)


class ProductCategRel(models.Model):
    _name = 'pos.product.category.rel'
    _description = 'Pos categories rel'

    product_tmpl_id = fields.Many2one(
        'product.template'
    )
    pos_category_id = fields.Many2one(
       'pos.category'
    )


class ProductCategAddRel(models.Model):
    _name = 'pos.product.category.add.rel'
    _description = 'Pos categories add rel'

    product_tmpl_id = fields.Many2one(
        'product.template'
    )
    pos_category_id = fields.Many2one(
       'pos.category'
    )

