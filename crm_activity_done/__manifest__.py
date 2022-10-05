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
        'views/mail_message_views.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
}
