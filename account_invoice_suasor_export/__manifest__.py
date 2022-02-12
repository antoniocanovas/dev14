{
    'name': 'Account Invoice Suasor Export',
    'version': '14.0.1.0.1',
    'category': '',
    'summary': """
            Exporta facturas de Odoo a formato Suasor
        """,
    'author': 'Serincloud',
    'depends': [
        'base_automation',
        'sql_export',
    ],
    'data': [
        'views/suasor_invoice_views.xml',
        'data/create_suasor_invoice.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
