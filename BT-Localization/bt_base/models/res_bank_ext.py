##############################################################################
#
# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
##############################################################################
from odoo import models


class ResBankExt(models.Model):
    _inherit = 'res.partner.bank'

    _sql_constraints = [
        ('unique_number', 'unique(sanitized_acc_number, l10n_ch_postal, company_id)',
         'Account Number - ISR reference combination must be unique'),
    ]
