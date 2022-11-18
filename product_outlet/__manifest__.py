{
    'name': 'Product Outlet',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
Sell refubished products in Spain (special taxes)
""",
    'author': 'Serincloud',
    'depends': [
        'base_automation',
        'sale_management',
        'purchase',
        'stock',
        'account',
        'crm_product',
    ],
    'data': [
        'views/model_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
}
