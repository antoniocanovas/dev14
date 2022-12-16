{
    'name': 'HR Expense detail',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
Hr Expense several tickets in one expense form
""",
    'author': 'Serincloud',
    'depends': [
        'hr_expense',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_expense_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
}
