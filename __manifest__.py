# -*- coding: utf-8 -*-
{
    'name': "Custom Module",
    'summary': """
        Module for custom views and models""",
    'author': "Kevin Marvin Calda",
    'category': 'Extra tool',
    'version': '0.1',
    'license': 'AGPL-3',
    'sequence': 10,
    'depends': ['base', 'sale_management', 'stock','contacts', 'account'],
    'data': [
        'views/custom_views.xml',
    ],
    'application': True,
    'installation': True,
    'auto_install': False,
}