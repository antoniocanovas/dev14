{
    'name': 'Account Invoice Suasor Export',
    'version': '12.0.2.0.1',
    'category': '',
    'summary': """
            Exporta facturas de Odoo a formato Suasor
        """,
    'author': 'Serincloud',
    'depends': [
        'base_automation',
    #    'account_cancel',
    #    'web_export_view',
    ],
    'data': [
        'views/suasor_invoice_views.xml',
        'data/create_suasor_invoice.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
