{
    'name': 'External Work',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
External Work
""",
    'author': 'Serincloud',
    'depends': [
        'sale_timesheet',
    ],
    'data': [
#        'data/action_server.xml',
        'security/ir.model.access.csv',
        'views/external_work_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
}
