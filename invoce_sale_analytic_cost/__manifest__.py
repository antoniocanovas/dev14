{
    'name': 'Invoice sale auto analytic cost',
    'version': '14.0.0.0.1',
    'category': '',
    'description': u"""
Crea apuntes analíticos con precio de coste a partir de la aceptación de la factura de venta.
""",
    'author': 'Serincloud',
    'depends': [
        'analytic',
    ],
    'data': [
        'views/product_template_views.xml',
    ],
    'installable': True,
}
