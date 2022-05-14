# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################

{
    "name": "Project Workshop",
    "version": "14.0.1.0.0",
    "category": "Project",
    "author": "Serincloud"
              "Antonio Cánovas (antonio.canovas@ingenieriacloud.com)",
    "maintainer": "Serincloud",
    "website": "www.ingenieriacloud.com",
    "license": "AGPL-3",
    "depends": [
        "project",
        "sale_timesheet",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/rule_project_workshop.xml",
        "views/project_workshop_view.xml",
        "views/menu_view.xml",

    ],
    "installable": True,
}
