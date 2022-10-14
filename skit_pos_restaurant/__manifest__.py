# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Skit POS Restaurant",
    'version': '1.1',
    'summary': """ POS Restaurant """,
    'license': "AGPL-3",
    'website': 'http://www.srikeshinfotech.com',
    'images': ['images/main_screenshot.png'],
    'description': """
        POS Restaurant
    """,

    'depends': ['point_of_sale', 'bus', "pos_restaurant",
                "skit_pos_floor_screen",
                "sale"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/pos_config_view.xml",
        "views/point_of_sale.xml",
        "views/pos_longpolling_template.xml",
        "data/pos_multi_session_data.xml",
        "security/ir.model.access.csv",
        "views/pos_multi_session_views.xml",
        "multi_session_view.xml",
        "views/views.xml",
        'views/pos_template.xml',
        'views/return.xml',
        'views/res_users_view.xml',
        'data/pos_expiry_date.xml',
        'data/pos_scheduler.xml',
        'views/pos_category_view.xml'
    ],
    'qweb': [
        "static/src/xml/pos_vendor_view.xml",
        "static/src/xml/pos_longpolling_connection.xml",
        "static/src/xml/pos_multi_session.xml",
        "static/src/xml/pos_restaurant.xml",
        'static/src/xml/pos_return.xml',
        ],
#     "demo": [
#         "demo/demo.xml"
#     ],
    "post_load": None,
    'installable': True,
    'auto_install': False,
    'application': True,
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',

}
