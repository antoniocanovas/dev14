# Copyright (C) Softhealer Technologies.
# Part of Softhealer Technologies.

{
    "name": "POS Multi Categories | Point Of Sale Multiple Categories",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Point of Sale",
    "license": "OPL-1",
    "summary": "POS Multiple Category, Point Of Sale Multi Category,POS Product Multiple Category,POS Product Multi Category,Multi categories in POS,Odoo POS Multi-Category,POS Extra Category,Point Of Sale Extra Category,POS Product Categories Odoo",
    "description": """Currently, in odoo, you can select only one category for a product in POS. The module allows to select the multiple POS categories per product. So you can manage your products easily with multiple categories.""",
    "version": "14.0.1",
    "depends": ["point_of_sale"],
    "application": True,
    "data": [
        'views/assets.xml',
        'views/sh_pos_product_config.xml',
    ],
    "qweb": [],
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
    "price": 25,
    "currency": "EUR"
}
