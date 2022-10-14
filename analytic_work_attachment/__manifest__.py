# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Antonio Cánovas antonio.canovas@serincloud.com
##############################################################################

{
    "name": "Sale attachment in Invoice",
    "version": "14.0.1.0.0",
    "category": "Account",
    "author": "www.serincloud.com",
    "maintainer": "Antonio Cánovas",
    "website": "www.serincloud.com",
    "license": "AGPL-3",
    "depends": [
        'account',
        'sale_management',
    ],
    "data": [
        'views/stock_move_line_views.xml'
    ],
    "installable": True,
}
