##############################################################################
#
# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
##############################################################################

from odoo import api, models


class AccountInvoiceExt(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        # OVERRIDE
        # Fill up field ref of account.move with value from l10n_ch_isr_number
        # This is needed for matching when import camt.054 file
        res = super(AccountInvoiceExt, self).action_invoice_open()
        for invoice in self:
            invoice.move_id.ref = invoice.l10n_ch_isr_number
        return res
