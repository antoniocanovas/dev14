from odoo import fields, models


class PosCategoryMulti(models.Model):
    _inherit = "product.template"

    pos_category_ids = fields.Many2many(
        "pos.category",
        string="Addtional categories",
        help="Those categories are used too, to group similar products for point of sale.",
    )
