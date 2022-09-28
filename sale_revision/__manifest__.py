{
    'name': "Sale Order Revision IC",
    'summary': """
        Create sale order revision with secuential code.
        Internal tab with other revisions and chatter messages.
        """,
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '14.0.1.0.0',
    'depends': [
        'sale_management', 'web_widget_open_tab',
    ],
    'data': [
        'views/views.xml',
        #'data/create_revision.xml',
    ],
    'installable': True,
    'application': False,
}
