# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################

{
    "name": "Product customizations",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "author": "Comunitea",
    "maintainer": "Serincloud",
    "website": "www.ingenieriacloud.com",
    "license": "AGPL-3",
    "depends": [
        "product",
        "purchase",
        "stock",
        "crm",
        "product_chassis",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product.xml",
        "views/stock.xml",
        "views/product_dictionary_views.xml",
        "views/menu_views.xml",
    ],
    "installable": True,
}
