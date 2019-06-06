##############################################################################
#
# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
##############################################################################
from odoo import models, fields, api, _
import re
from odoo.tools import mod10r
from odoo import exceptions


class ResBankExt(models.Model):
    """ Inherit res.bank class in order to add swiss specific fields

        Fields from the original file downloaded from here:
        https://www.six-group.com/interbank-clearing/de/home/bank-master-data/download-bc-bank-master.html

        ==   =============   ================
        #    Field in file   Column
        --   -------------   ----------------
        11   Kurzbez.        code
        21   Postkonto       ccp
        3    BCNr neu        bank_clearing_new
        5    Hauptsitz       bank_headquarter
        13   Domizil         street
        0    Gruppe          bank_group
        16   Ort             city
        15   PLZ             zip
        1    BCNr            clearing
        19   Vorwahl         bank_areacode
        6    BC-Art          bank_bcart
        9    euroSIC         bank_eurosic
        4    SIC-Nr          bank_sicnr
        22   SWIFT           bic
        2    Filial-ID       bank_branchid
        8    SIC             bank_sic
        17   Telefon         phone
        10   Sprache         bank_lang
        14   Postadresse     bank_postaladdress
        12   Bank/Institut   name
        20   Landcode        country
        7    gültig ab       bank_valid_from
        18   Fax             NO_IMPORT
        ==   =============   ================

        .. note:: Postkonto: ccp does not allow to enter entries like
           ``*30-38151-2`` because of the ``*`` but this comes from the
           xls to import
        """
    _inherit = 'res.bank'

    bank_group = fields.Char(string='Group', size=2)
    bank_branchid = fields.Char(string='Branch-ID', size=5)
    bank_clearing_new = fields.Char(string='BCNr new', size=5)
    bank_sicnr = fields.Char(string='SIC-Nr', size=6)
    bank_headquarter = fields.Char(string='Headquarter', size=5)
    bank_bcart = fields.Char(string='BC-Art', size=1)
    bank_valid_from = fields.Date(string='Valid from')
    bank_sic = fields.Char(string='SIC', size=1)
    bank_eurosic = fields.Char(string='euroSIC', size=1)
    bank_lang = fields.Char(string='Language', size=1)
    bank_postaladdress = fields.Char(string='Postal address', size=35)
    bank_areacode = fields.Char(string='Area code', size=5)
    bank_postaccount = fields.Char(string='Post account', size=35)
    code = fields.Char(
        string='Code',
        help='Internal reference'
    )
    clearing = fields.Char(
        string='Clearing number',
        help='Swiss unique bank identifier also used in IBAN number'
    )
    city = fields.Char(
        string='City',
        help="City of the bank"
    )
    ccp = fields.Char(
        string='CCP/CP-Konto',
        size=11,
        help="CCP/CP-Konto of the bank"
    )
    country_code = fields.Char(
        string="Country code",
        related="country.code",
        readonly=True,
    )

    def is_swiss_postal_num(self, number):
        return (self._check_9_pos_postal_num(number) or
                self._check_5_pos_postal_num(number))

    def _check_9_pos_postal_num(self, number):
        """
        Predicate that checks if a postal number
        is in format xx-xxxxxx-x is correct,
        return true if it matches the pattern
        and if check sum mod10 is ok

        :param number: postal number to validate
        :returns: True if is it a 9 len postal account
        :rtype: bool
        """
        pattern = r'^[0-9]{2}-[0-9]{1,6}-[0-9]$'
        if not re.search(pattern, number):
            return False
        nums = number.split('-')
        prefix = nums[0]
        num = nums[1].rjust(6, '0')
        checksum = nums[2]
        expected_checksum = mod10r(prefix + num)[-1]
        return expected_checksum == checksum

    def _check_5_pos_postal_num(self, number):
        """
        Predicate that checks if a postal number
        is in format xxxxx is correct,
        return true if it matches the pattern
        and if check sum mod10 is ok

        :param number: postal number to validate
        :returns: True if is it a 5 len postal account
        :rtype: bool
        """
        pattern = r'^[0-9]{1,5}$'
        if not re.search(pattern, number):
            return False
        return True

    @api.constrains('ccp')
    def _check_postal_num(self):
        """Validate postal number format"""
        for bank in self:
            if not bank.ccp:
                continue
            if not self.is_swiss_postal_num(bank.ccp):
                raise exceptions.ValidationError(
                    _('Please enter a correct postal number. '
                      '(01-23456-1 or 12345)')
                )
        return True

    @api.multi
    def name_get(self):
        """Format displayed name"""
        res = []
        cols = ('bic', 'name', 'street', 'city')
        for bank in self:
            vals = (bank[x] for x in cols if bank[x])
            res.append((bank.id, ' - '.join(vals)))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=80):
        """Extends to look on bank code, bic, name, street and city"""
        if args is None:
            args = []
        ids = []
        cols = ('code', 'bic', 'name', 'street', 'city')
        if name:
            for val in name.split(' '):
                for col in cols:
                    tmp_ids = self.search(
                        [(col, 'ilike', val)] + args,
                        limit=limit
                    )
                    if tmp_ids:
                        ids += tmp_ids.ids
                        break
        else:
            ids = self.search(
                args,
                limit=limit
            ).ids
        # we sort by occurence
        to_ret_ids = list(set(ids))
        to_ret_ids = sorted(
            to_ret_ids,
            key=lambda x: ids.count(x),
            reverse=True
        )
        return self.browse(to_ret_ids).name_get()
