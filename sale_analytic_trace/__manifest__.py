{
    'name': 'Sale Analytic Tracing',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
Compares sold productos with analytic inputs.
""",
    'author': 'Serincloud',
    'depends': [
        'sale_management',
        'analytic',
        'base_automation',
        'sale_mrp_bom',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/action_server.xml',
    ],
    'installable': True,
}
