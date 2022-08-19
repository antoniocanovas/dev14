{
    'name': 'Sale target',
    'version': '14.0.1.0',
    'category': 'Sale',
    'description': u"""
Sales anual target per commercial.
Quarter resume.
""",
    'author': 'Serincloud',
    'depends': [
        'sale_management',
        'crm',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/server_action.xml',
        'views/target_views.xml',
        'views/views_menu.xml',
    ],
    'installable':True,
}
