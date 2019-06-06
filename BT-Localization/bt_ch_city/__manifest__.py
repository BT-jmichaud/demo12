##############################################################################
#
# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
##############################################################################
{
    'name': 'Switzerland - All cities',
    'version': '12.0.1.0.0',
    'author': 'brain-tec AG',
    'category': 'Localisation',
    'website': 'http://www.braintec-group.com',
    'license': 'AGPL-3',
    'summary': 'Provides all swiss cities for auto-completion',
    'depends': [
        'base_address_city',
        'contacts',
        'bt_ch_state',  # in https://github.com/brain-tec/bt_ch_state
    ],
    'data': ['data/res.city.csv'],
    'images': [],
    'demo': [],
    'auto_install': False,
    'installable': True,
    'application': True,
}
