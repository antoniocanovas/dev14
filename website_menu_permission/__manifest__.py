# Copyright 2023 SERINCLOUD SL
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    'name': 'Website Menu Permission',
    'version': '14.0.1.0.0',
    'author': 'Serincloud SL',
    'website': 'https://github.com/OCA/website',
    'license': 'LGPL-3',
    'category': 'Website',
    'summary': 'Avoid loosing admin acces to website menu when selecting portal or public group.',
    'depends': [
        'website',
    ],
    'data': [
        'security/record_rules.xml',
    ],
    'installable': True,
}
