# Copyright 2022 IC - Serincloud
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Custom Masiste",
    "summary": "",
    "version": "14.0.1.0.0",
    "category": "Customization",
    "author": "Serincloud",
    "website": "",
    "license": "AGPL-3",
    "depends": ['crm',
                'base_automation',
                'sale_management',
                'helpdesk_mgmt',
                'partner_expired_debt',],
    "data": [
        "views/crm_lead_view.xml",
        "views/sale_order_view.xml",
        "views/helpdesk_ticket_view.xml",
        "views/res_partner.xml",
        "data/action_server.xml",
    ],
    "installable": True,
}
