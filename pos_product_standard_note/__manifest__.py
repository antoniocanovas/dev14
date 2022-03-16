# -*- coding: utf-8 -*-
{
    'name': "POS Product Standard Note",
    'summary': """
       POS Product Standard Note""",
    'description': """
        POS Product Standard Note
    """,
    'website': "https://www.ingenieriacloud.com",
    'author': "Serincloud SL",
    'category': 'Point of Sale',
    'version': '14.0.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['point_of_sale', 'pos_restaurant'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/pos_note_views.xml',
        'views/pos_note_type_views.xml',
        'views/product_product_views.xml',
        'views/pos_order_views.xml',
    ],
    'qweb': [
        'static/src/xml/Popups/TextAreaPopup.xml',
        'static/src/xml/Screens/ReceiptScreen/OrderReceipt.xml',
    ],
}
