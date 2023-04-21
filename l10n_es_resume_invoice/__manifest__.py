{
    'name': 'POS Resume Invoice',
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
        'views/resume_invoice_views.xml',
    ],
    'installable': True,
}
