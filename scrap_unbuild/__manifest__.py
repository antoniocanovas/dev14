# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################

{
    "name": "Scrap Unbuild",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "author": "www.serincloud.com",
    "maintainer": "Pedroguirao",
    "website": "www.serincloud.com",
    "license": "AGPL-3",
    "depends": [
        'purchase',
        'sale_management',
        'stock',
        'account',
        'analytic',
        'project',
        'hr_timesheet',
        'base_automation',
        'product_analytic',
        'product_chassis',
    ],
    "data": [
        "views/product.xml",
        "views/menu_views.xml",
        "views/res_company.xml",
        "data/action_server.xml",
        "data/sequence.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
