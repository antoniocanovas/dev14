{
    'name': 'POS product sequence',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
    Product sequence field in product view, change this value to set product order view in pos environment.
""",
    'author': 'Serincloud',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'views/product_views.xml',
    ],
    'installable': True,
}
