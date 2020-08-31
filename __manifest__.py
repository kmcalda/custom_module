# -*- coding: utf-8 -*-
{
    'name': "Custom Module",
    'summary': """
        Module for custom views and models""",
    'website': 'https://github.com/kmcalda/custom_module',
    'author': "Kevin Marvin Calda",
    'category': 'Extra tool',
    'version': '0.1',
    'license': 'AGPL-3',
    'sequence': 10,
    'depends': ['base', 'sale_management', 'stock', 'contacts', 'account', 'mail', 'web'],
    'data': [
        'views/custom_views.xml',
        'views/salesperson_code.xml',
        'template/review_email_template.xml',
        'template/send_to_email_test.xml',
        'security/ir.model.access.csv',
        'groups/custom_group.xml',
        'security/security.xml',
    ],
    'application': True,
    'installation': True,
    'auto_install': False,
}