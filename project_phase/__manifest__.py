{
    'name': 'Project business phases',
    'version': '14.0.0.1',
    'category': 'Projects',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'crm',
        'project',
        'sale_management',
        'purchase',
        'stock',
        'account',
        'base_automation',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/project_view.xml',
        'views/project_phase_view.xml',
        'views/views_menu.xml',
    ],
    'installable':True,
}
