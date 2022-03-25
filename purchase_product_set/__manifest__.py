# Copyright 2015 Anybox
# Copyright 2018 Camptocamp, ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase product set",
    "category": "Purchase",
    "license": "AGPL-3",
    "author": "Anybox, Odoo Community Association (OCA)",
    "version": "14.0.1.0.0",
    "website": "https://github.com/OCA/purchase-workflow",
    "summary": "Purchase product set",
    "depends": ["sale_product_set","purchase"],
    "data": [
        "security/ir.model.access.csv",
        "security/rule_product_set.xml",
        "views/purchase_product_set.xml",
        "views/purchase_product_set_line.xml",
        "wizard/product_set_add.xml",
        "views/purchase_order.xml",
    ],
    "demo": ["demo/product_set.xml", "demo/product_set_line.xml"],
    "installable": True,
}
