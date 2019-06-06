##############################################################################
#
# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
##############################################################################
{
    'name': 'BT CH Localization - Base Module',
    'version': '12.0.1.0.1',
    'author': 'brain-tec AG',
    'category': 'Localisation',
    'website': 'http://www.braintec-group.com',
    'license': 'AGPL-3',
    'summary': 'Provides support for CH Localization',
    'depends': [
        'base',
        'account',
        'contacts',
        'l10n_ch',
    ],
    'images': [],
    'demo': [],
    'data': [
        'views/res_partner_views_ext.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
