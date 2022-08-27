{
    'name': 'Product Outlet (original)',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
Sell refubished products in Spain (special taxes)
""",
    'author': 'Serincloud',
    'depends': [
        'fleet_vehicle_category',
        'sale_management',
        'purchase',
        'analytic',
        'stock',
        'account',
        'base_automation',
        'product_analytic',
        'crm_product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/action_server.xml',
        'data/sequence.xml',
        'views/model_views.xml',
        'views/menu_views.xml',
    ],
    'installable': False,
}
