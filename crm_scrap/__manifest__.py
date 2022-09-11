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
        'views/crm_lead_views.xml',
        'views/project_task_views.xml',
    ],
    'installable': True,
}
