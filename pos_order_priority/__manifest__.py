# Copyright 2019 LevelPrime
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "POS order priority",
    "summary": "Add button to set priority to orders.",
    "author": "Pedro Guirao, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/pos",
    "category": "Point of Sale",
    "maintainers": ["pedroguirao"],
    "version": "14.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["pos_restaurant",],
    "data": [
        "views/assets.xml",
        "data/pos_order_line_priority.xml",
        "views/pos_config_view.xml",
        "security/ir.model.access.csv",
             ],
    "qweb": [
        "static/src/xml/orderline.xml",
        "static/src/xml/multiprint.xml",
        "static/src/xml/ProductScreen/ControlButtons/SetPriorityButton.xml",
             ],
}
