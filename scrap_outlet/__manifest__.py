{
    'name': 'SCRAP Outlet',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
Sell refubished products in Spain (special taxes)
""",
    'author': 'Serincloud',
    'depends': [
        'purchase_donation',
        'product_outlet',
        'fleet_vehicle_category',
        'base_automation',
    ],
    'data': [
        'data/action_server.xml',
        'views/timesheet_work_views.xml',
    ],
    'installable': True,
}
