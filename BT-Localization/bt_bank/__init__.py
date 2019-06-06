##############################################################################
#
# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
##############################################################################
from . import models

def post_init(cr, registry):
    """Import CSV data as it is faster than xml and because we can't use
    noupdate anymore with csv"""
    from odoo.tools import convert_file
    print('::post_init()', locals())
    filename = 'data/res.bank.csv'
    convert_file(cr, 'bt_bank', filename, None, mode='init',
                 noupdate=True, kind='init', report=None)