{
    'name': 'Product Outlet',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
Sell refubished products in Spain (special taxes)
""",
    'author': 'Serincloud',
    'depends': [
        'sale_management',
        'purchase',
        'stock',
        'account',
        'crm_product',
    ],
    'data': [
        'views/timesheet_work_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
}
