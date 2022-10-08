{
    'name': 'Timesheet Work Extended',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'hr_timesheet_work',
        'hr_equipment_stock',

    ],
    'data': [
        'security/ir.model.access.csv',
        'views/model_views.xml',
    ],
    'installable': True,
}
