##############################################################################
#
# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
##############################################################################
from odoo import models, fields, api
from odoo.osv import expression


class ResCityExt(models.Model):
    """ Inherit res.city class in order to add swiss specific fields """

    _inherit = 'res.city'

    name_short = fields.Char("Name short", translate=True)
    g_zipcode = fields.Char("GZip")

    active = fields.Boolean(string='Active', default=True)
    onrp = fields.Char(string='Swiss Post classification no. (ONRP)',
                       size=5, help="Primary Key")
    zip_type = fields.Char(string='Postcode type', size=2)
    additional_digit = fields.Char(string='Additional poscode digits', size=2)
    lang = fields.Char(
        string='Language code', size=1,
        help="Language (language majority) within a postcode area. "
             "1 = German, 2 = French, 3 = Italian, 4 = Romansh. "
             "For multi-lingual localities, the main language is indicated.",
    )
    lang2 = fields.Char(
        'Alternative language code',
        size=1,
        help="Additional language within a postcode.\n"
             "One alternative language code may appear for each postcode.\n"
             "1 = German, 2 = French, 3 = Italian, 4 = Romansh.",
    )
    sort = fields.Boolean(
        string='Present in sort file',
        help="Indicates if the postcode is included in the «sort file»"
             "(MAT[CH]sort): 0 = not included, 1 = included. "
             "Delivery information with addresses (only postcode and "
             "streets) are published in the sort file.",
    )
    post_delivery_through = fields.Integer(
        string='Mail delivery by',
        size=5,
        help="Indicates the post office (ONRP) that delivers most of the "
             "letters to the postcode addresses. This information can be "
             "used for bag addresses too."
    )
    zip_post_delivery = fields.Integer(
        string='ZIP Mail delivery',
        size=6,
        help="Indicates the post office (ONRP) that delivers most of the "
             "letters to the postcode addresses. This information can be "
             "used for bag addresses too."
    )
    communitynumber_bfs = fields.Integer(
        string='FSO municipality number (BFSNR)',
        size=5,
        help="Numbering used by the Federal Statistical Office for "
             "municipalities in Switzerland and the Principality of "
             "Liechtenstein",
    )
    valid_from = fields.Char(string='Valid from', size=8)

    _sql_constraints = [
        ('zipcode_name_state_country_uniq',
         'UNIQUE(zipcode, name, state_id, country_id)',
         'You already have a city with that name and zipcode in the same state.'
         'The city must have a unique name and postcode within '
         'it\'s state and it\'s country'),
    ]

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100,
                     name_get_uid=None):
        args = args or []
        domain = []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            domain = ['|', ('zipcode', operator, name),
                      ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        city_ids = self._search(domain + args, limit=limit,
                                access_rights_uid=name_get_uid)
        return self.browse(city_ids).name_get()
