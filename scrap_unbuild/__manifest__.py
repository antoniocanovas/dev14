# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Antonio Cánovas antonio.canovas@ingenieriacloud.com
##############################################################################

{
    "name": "Scrap Unbuild",
    "version": "14.0.3.0.0",
    "category": "Sales",
    "author": "www.serincloud.com",
    "maintainer": "Pedroguirao",
    "website": "www.serincloud.com",
    "license": "AGPL-3",
    "depends": [
        'purchase',
        'sale_timesheet',
        'stock',
        'account',
        'analytic',
        'base_automation',
        'product_analytic',
        'product_brand',
x        'product_chassis',
    ],
    "data": [
        "data/action_server.xml",
        "data/action_server_wizard.xml",
        "views/scrap_unbuild_wizard.xml",
        "views/product.xml",
        "views/menu_views.xml",
        "views/res_company.xml",
        "data/sequence.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
