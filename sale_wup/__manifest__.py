{
    'name': 'WUP',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'sale_management',
        'product_brand',
        'hr',
        'base_automation',
        'sale_timesheet_edit',
    ],
    'data': [
        'data/server_action.xml',
        'data/automated_action.xml',
        'security/ir.model.access.csv',
        'views/model_views.xml',
        'views/menu_views.xml',
        'views/sale_order_views.xml',
        'views/product_views.xml',
        'views/project_task.xml',
    ],
    'installable': True,
}
