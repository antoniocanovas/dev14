{
    'name': 'Work base',
    'version': '14.0.6.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'base_automation',
        'sale_timesheet',
        'repair',
        'mrp',

    ],
    'data': [
        'security/ir.model.access.csv',
        'data/action_server.xml',
        'data/data.xml',
        'data/rules.xml',
        'views/model_views.xml',
        'views/menu_views.xml',
        'views/templates.xml',
        'views/work_sheet_report.xml',
    ],
    'installable': True,
}
