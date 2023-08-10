{
    'name': 'CRM SCRAP',
    'version': '14.0.2.0.0',
    'category': '',
    'description': u"""
SCRAP demand integration from CRM
""",
    'author': 'Serincloud',
    'depends': [
        'crm',
        'project',
        'product_brand',
        'web_widget_open_tab',
        'web_tree_dynamic_colored_field',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/crm_stage_views.xml',
        'views/project_task_views.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
}
