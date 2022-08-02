{
    'name': "Equipment Services",
    'summary': """
        Services by maintenance equipment.
        """,
    'author': "Serincloud SL",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '14.0.1.0.0',
    'depends': [
        'maintenance',
    ],
    'data': [
        'views/views.xml',
        'views/views_menu.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}
