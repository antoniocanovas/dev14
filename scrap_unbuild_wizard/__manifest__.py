{
    'name': 'Scrap Unbuild Wizard',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
Scrap Unbuild Wizard to Stock Inventory
""",
    'author': 'Serincloud',
    'depends': [
        'scrap_unbuild',
    ],
    'data': [
        'data/server_actions.xml',
        'views/scrap_unbuild_wizard.xml',
        'views/product_template_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
