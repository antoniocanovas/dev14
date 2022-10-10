{
    'name': 'Timesheet Work base',
    'version': '14.0.7.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'base_automation',
        'purchase',
        'stock',
        'sale_timesheet',
        'hr_timesheet_time_type',
        'hr_timesheet_activity_begin_end',
        'analytic_line_tracking',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/rules.xml',
        'data/action_server.xml',
        'views/timesheet_work_views.xml',
        'views/work_sheet_views.xml',
        'views/account_analytic_tag_views.xml',
        'views/account_analytic_line_views.xml',
        'views/stock_picking_views.xml',
        'views/templates.xml',
        'views/work_sheet_report.xml',
        'views/hr_employee.xml',
        'views/timesheet_line_todo_views.xml',
        'views/timesheet_line_done_views.xml',
        'views/sale_order_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
}
