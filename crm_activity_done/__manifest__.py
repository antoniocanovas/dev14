{
    'name': 'CRM Activity done',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
CRM Activity done based on mail.messages
""",
    'author': 'Serincloud',
    'depends': [
        'crm',
    ],
    'data': [
        'views/mail_message_views.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
}
