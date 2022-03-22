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
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/stock_move_view.xml',
        'views/stock_picking_view.xml',
    ],
    'installable':True,
}
