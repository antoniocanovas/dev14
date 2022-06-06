{
    'name': 'Invoice from origin',
    'version': '14.0.0.1',
    'category': 'Account',
    'description': u""Permite facturación de obras en origen desde una factura generada desde el pedido de venta,
                teniendo en cuenta los conceptos ya facturados, según solicitan constructuras."""",
    'author': 'Serincloud',
    'depends': [
        'sale_management',
        'account',
        'analytic',
    ],
    'data': [
        'views/sale_order_view.xml',
        'data/server_action.xml',
    ],
    'installable':True,
}
