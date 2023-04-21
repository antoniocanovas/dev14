{
    'name': 'POS Resume Invoice',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
Crear facturas resumen de tickets históricos.
""",
    'author': 'Serincloud',
    'depends': [
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/resume_invoice_views.xml',
    ],
    'installable': True,
}
