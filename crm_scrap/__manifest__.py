{
    'name': 'CRM SCRAP',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
SCRAP demand integration in CRM
""",
    'author': 'Serincloud',
    'depends': [
        'crm',
        'project',
        'product_brand',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/project_task_views.xml',
        'views/res_company_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
}
