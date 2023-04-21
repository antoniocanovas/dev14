{
    'name': 'Partner Activity done',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
Partner Activities done based on mail.messages
""",
    'author': 'Serincloud',
    'depends': [
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/resume_invoice_views.xml',
    ],
    'installable': True,
}
