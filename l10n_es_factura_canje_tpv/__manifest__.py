{
    'name': 'Facturas de canje en TPV',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
Facturas de canje para TPV.
""",
    'author': 'Serincloud',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/menu_views.xml',
        'views/factura_canje_views.xml',
        'views/pos_order_views.xml',
    ],
    'installable': True,
}
