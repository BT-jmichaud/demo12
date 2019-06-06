#!/usr/bin/python
import subprocess
import sys
import zipfile
try:
    import pandas as pd
except ImportError:
    pd = None
import os
sys.path.append('../../odoo/odoo/tools/')

# Execution: python3.5 ./create_new_res_bank_csv.py

new_zip_file_name = 'bankenstamm.zip'
command = 'curl -o %s -i --basic -H "Content-Type: application/octet-stream" -X GET ' \
          '"https://www.six-group.com/interbank-clearing/dam/downloads/bc-bank-master/bcbankenstamm_d.zip"' \
          % (new_zip_file_name)
try:
    # this is downloading the latest gateway file and saves it as gateway.zip in the current folder
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
except:
    print('Error in command: ', command)

try:
    with zipfile.ZipFile(new_zip_file_name, "r") as zf:
        for name in zf.namelist():
            localFilePath = zf.extract(name, '/tmp/')
            if os.path.isdir(localFilePath):
                continue

            import codecs

            sourceFileName = localFilePath
            xls_file = pd.read_excel(sourceFileName, sheet_name=0)
            sourceFileName_csv = sourceFileName.replace('.xls', '.csv')
            xls_file.to_csv(sourceFileName_csv, index=False)

            targetFileName = '/tmp/test_bank.csv'
            newFileName = '/tmp/new_bank_data.csv'
            BLOCKSIZE = 1048576  # or some other, desired size in bytes
            with codecs.open(sourceFileName_csv, "r", "utf-8") as sourceFile:
                # Edit: this only works with python 2.x.
                # To make it work with python 3.x replace wb by w
                with codecs.open(targetFileName, "w", "utf-8") as targetFile:
                    while True:
                        contents = sourceFile.read(BLOCKSIZE)
                        if not contents:
                            break
                        targetFile.write(contents)

            import csv

            with open(newFileName, 'w', encoding='utf-8') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',)

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
                # id,code,ccp,bank_clearing_new,bank_headquarter,street,bank_group,city,zip,clearing,bank_areacode,
                # bank_bcart,bank_eurosic,bank_sicnr,bic,bank_branchid,bank_sic,phone,active,bank_lang,
                # bank_postaladdress,name,country,bank_valid_from

                # l10n_ch_bank.bank_80532_0003,Raiffeisen,19-1527-5,,80000,Alte Simplonstrasse 35,8,
                # Simplon Dorf,3907,80532,,3,1,80000,RAIFCH22532,3,1,027 979 12 21,True,1,,
                # Raiffeisenbank Belalp-Simplon,Switzerland,,

                # csv from six
                # 0 Gruppe	1 BCNr	2 Filial-ID	3 BCNr neu	4 SIC-Nr	5 Hauptsitz	6 BC-Art	7 gültig ab	8 SIC
                # 9 euroSIC	10 Sprache	11 Kurzbez.	12 Bank/Institut	13 Domizil	14 Postadresse	15 PLZ	16 Ort
                # 17 Telefon	18 Fax	19 Vorwahl	20 Landcode	21 Postkonto	22 SWIFT
                # 08805320003	80532380000320110813111Raiffeisen	Raiffeisenbank Belalp-Simplon
                # Alte Simplonstrasse 35	3907	Simplon Dorf	027 979 12 21	027 979 14 71	*19-1527-5
                # RAIFCH22532

                # open file
                count_added = 0
                XML_ID_TEMP = 'bt_bank.bank_'
                with open(sourceFileName_csv, 'rt', encoding="utf-8") as f:
                    reader = csv.reader(f)
                    filewriter.writerow(('id,code,ccp,bank_clearing_new,bank_headquarter,street,bank_group,city,'
                                         'zip,clearing,bank_areacode,bank_bcart,bank_eurosic,bank_sicnr,bic,'
                                         'bank_branchid,bank_sic,phone,active,bank_lang,bank_postaladdress,name,'
                                         'country,bank_valid_from').split(','))
                    # read file row by row
                    next(reader)
                    for row in reader:
                        if len(row) > 0:
                            new_row = [''] * 24
                            # clearing_ ('4835_0154')
                            XML_ID = XML_ID_TEMP + row[1] + '_' + row[2].zfill(4)
                            new_row[0] = XML_ID
                            new_row[1] = row[11]
                            # ccp does not allow to enter entries like ``*30-38151-2`` because of the ``*``
                            # but this comes from the xls to import
                            new_row[2] = row[21].replace('*', '')
                            new_row[3] = row[3]
                            new_row[4] = row[5]
                            new_row[5] = row[13]
                            new_row[6] = row[0]
                            new_row[7] = row[16]
                            new_row[8] = row[15]
                            new_row[9] = row[1]
                            new_row[10] = row[19]
                            new_row[11] = row[6]
                            new_row[12] = row[9]
                            # SIC-NR:    6-Stellig mit Nullen Links auffüllen
                            new_row[13] = row[4].zfill(6)
                            new_row[14] = row[22]
                            # Filial-ID: 4-Stellig mit Nullen Links auffüllen
                            new_row[15] = row[2].zfill(4)
                            new_row[16] = row[8]
                            new_row[17] = row[17]
                            new_row[18] = 'True'
                            new_row[19] = row[10]
                            new_row[20] = row[14]
                            new_row[21] = row[12]
                            new_row[22] = row[20]
                            if not new_row[22]:
                                new_row[22] = 'Switzerland'
                            if row[7]:
                                new_row[23] = '-'.join([row[7][:4], row[7][4:6], row[7][6:8]])
                            new_line = ";".join(new_row)
                            filewriter.writerow(new_line.split(';'))
                            count_added += 1

            a = pd.read_csv('data/res.bank.csv', usecols=['id'])
            b = pd.read_csv(newFileName, encoding='utf-8', usecols=['id'])
            c = pd.concat([a, b], axis=0, sort=False)

            c.drop_duplicates(keep=False,
                              inplace=True)  # Set keep to False if you don't want any
            # of the duplicates at all
            c.reset_index(drop=True, inplace=True)
            print(c)
            # Write to output file
            with open('different.csv', 'w') as file_out:
                c.to_string(file_out)


except Exception as err:
    print('(jool) err: ', err)
