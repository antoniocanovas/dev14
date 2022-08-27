{
    'name': 'SCRAP Outlet',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
Sell refubished products in Spain (special taxes)
""",
    'author': 'Serincloud',
    'depends': [
        'scrap_unbuild',
        'product_outlet',
        'fleet_vehicle_category',
        'base_automation',
    ],
    'data': [
        'data/action_server.xml',
        'views/model_views.xml',
    ],
    'installable': True,
}
