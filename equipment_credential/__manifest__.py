{
    'name': "Equipment credentials",
    'summary': """
        Services and credentials by maintenance equipment.
        """,
    'author': "Serincloud SL",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '14.0.1.0.1',
    'depends': [
        'partner_credentials',
        'maintenance',
        'equipment_service',
    ],
    'data': [
        'views/views.xml',
    ],
    'installable': True,
    'application': False,
}
