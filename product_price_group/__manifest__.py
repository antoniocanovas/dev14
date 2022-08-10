{
    'name': "Product prices group",
    'summary': """
        Hide prices to users not in sales, purchases and invoicing.
        """,
    'author': "Serincloud SL",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '14.0.1.0.0',
    'depends': [
        'product',
        'sale_management',
        'purchase',
        'account',
    ],
    'data': [
        'views/views.xml',
        'security/res_group.xml',
    ],
    'installable': True,
    'application': False,
}
