# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################

{
    "name": "Purchase price update",
    "version": "14.0.2.0.1",
    "category": "Sales",
    "author": "Serincloud",
    "maintainer": "Serincloud",
    "website": "www.serincloud.com",
    "license": "AGPL-3",
    "depends": [
        'purchase',
        'purchase_discount',
    ],
    "data": [
        "views/model_view.xml",
        "wizards/wizard_template.xml",
        "security/ir.model.access.csv",
        "security/user_groups.xml",
    ],
    "installable": True,
}
