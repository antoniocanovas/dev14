{
    'name': 'Procedures',
    'version': '14.0.0.1',
    'category': 'Projects',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'project',
        'sale_management',
        'purchase',
        'stock',
        'account',
        'base_automation',
    ],
    'data': [
#        'views/views.xml',
#        'views/views_menu.xml',
        'security/ir.model.access.csv',
        'views/project_view.xml',
    ],
    'installable':True,
}
