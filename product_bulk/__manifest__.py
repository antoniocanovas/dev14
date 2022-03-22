{
    'name': 'Product Bulk',
    'version': '14.0.0.1',
    'category': 'Stock',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'sale_management',
        'purchase',
        'stock',
        'account',
        'base_automation',
    ],
    'data': [
        'views/product_product_view.xml',
#        'views/stock_picking_view.xml',
    ],
    'installable':True,
}
