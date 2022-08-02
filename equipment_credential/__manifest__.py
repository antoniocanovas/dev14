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
    ],
    'data': [
        'views/views.xml',
        'views/views_menu.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
