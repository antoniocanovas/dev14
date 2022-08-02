{
    'name': "HelpDesk tickets link partner credentials",
    'summary': """
        Equipment service in helpdesk ticket.
        """,
    'author': "Serincloud SL",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '14.0.1.0.0',
    'depends': [
        'partner_credentials',
        'helpdesk_mgmt',
        'equipment_credential',
    ],
    'data': [
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
}
