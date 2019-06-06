##############################################################################
#
# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
##############################################################################
from odoo import fields, models


class CountryState(models.Model):
    _inherit = 'res.country.state'

    name = fields.Char(translate=True)
