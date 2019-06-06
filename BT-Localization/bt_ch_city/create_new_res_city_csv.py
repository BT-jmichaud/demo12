#!/usr/bin/python
# curl -o actual_gateway.zip -i --basic --user "TU_1415955_0001:xcSjPZ5B" -H
# "Content-Type: application/octet-stream" -X GET
# "https://webservices.post.ch:17017/IN_ZOPAxFILES/v1/groups/1062/versions/latest/file/gateway"

import subprocess
import sys
import zipfile
try:
    import pandas as pd
except ImportError:
    pd = None
import os
sys.path.append('../../odoo/odoo/tools/')

# HACK: 12.02.19 10:59: jool1: get info from bt password manager via url:
# https://passwd.braintec-group.com/index.php/pwd/view/1168

# Execution: python3.5 ./create_new_res_city_csv.py USERNAME PWD

new_zip_file_name = 'gateway.zip'
command = 'curl -o %s -i --basic --user "%s:%s" -H "Content-Type: application/octet-stream" -X GET ' \
          '"https://webservices.post.ch:17017/IN_ZOPAxFILES/v1/groups/1062/versions/latest/file/gateway"' \
          % (new_zip_file_name, sys.argv[1], sys.argv[2])
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
            targetFileName = '/tmp/test.csv'
            newFileName = '/tmp/new_city_data.csv'
            BLOCKSIZE = 1048576  # or some other, desired size in bytes
            with codecs.open(sourceFileName, "r", "ISO-8859-1") as sourceFile:
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
                filewriter = csv.writer(csvfile, delimiter=',',
                                        quoting=csv.QUOTE_MINIMAL)
                # id,zip_type,name,valid_from,onrp,communitynumber_bfs,country_id/id,sort,lang,lang2,
                # additional_digit,post_delivery_through,state_id/id,zipcode
                # zip_196,20,Dommartin,1989-06-01,196,5540,base.ch,1,2,,21,7670,bt_ch_state.state_VD,1041

                # csv from post
                # REC_ART	ONRP	BFSNR	PLZ_TYP	POSTLEITZAHL	PLZ_ZZ	GPLZ	ORTBEZ18	ORTBEZ27	KANTON
                # SPRACHCODE	SPRACHCODE_ABW	BRIEFZ_DURCH	GILT_AB_DAT	PLZ_BRIEFZUST	PLZ_COFF
                # 01;196;5540;20;1041;21;1041;Dommartin;Dommartin;VD;2;;7670;19890601;104060;J

                # open file
                count_added = 0
                with open(sourceFileName, 'rt', encoding="ISO-8859-1") as f:
                    reader = csv.reader(f)
                    filewriter.writerow(('id,communitynumber_bfs,zip_type,zipcode,additional_digit,g_zipcode,'
                                         'name_short,name,state_id/id,lang,lang2,post_delivery_through,valid_from,'
                                         'zip_post_delivery,sort,country_id/id,onrp').split(','))
                    # read file row by row
                    next(reader)
                    for row in reader:
                        row_data_splitted = row[0].split(';')
                        if row_data_splitted[0] == '01' and \
                                row_data_splitted[3] in ('10', '20'):
                            line = str(row)
                            line = line.replace("['", '["').replace("']", '"]')
                            new_line = line. \
                                replace('["01;', 'city_'). \
                                replace(';J"', ';1;base.ch"'). \
                                replace(';N"', ';0;base.ch"'). \
                                replace(';', ','). \
                                replace('"]', ""). \
                                replace(',AG,', ',bt_ch_state.state_AG,'). \
                                replace(',AI,', ',bt_ch_state.state_AI,'). \
                                replace(',AR,', ',bt_ch_state.state_AR,'). \
                                replace(',BE,', ',bt_ch_state.state_BE,'). \
                                replace(',BL,', ',bt_ch_state.state_BL,'). \
                                replace(',BS,', ',bt_ch_state.state_BS,'). \
                                replace(',DE,', ',bt_ch_state.state_DE,'). \
                                replace(',FL,', ',bt_ch_state.state_FL,'). \
                                replace(',FR,', ',bt_ch_state.state_FR,'). \
                                replace(',GE,', ',bt_ch_state.state_GE,'). \
                                replace(',GL,', ',bt_ch_state.state_GL,'). \
                                replace(',GR,', ',bt_ch_state.state_GR,'). \
                                replace(',IT,', ',bt_ch_state.state_IT,'). \
                                replace(',JU,', ',bt_ch_state.state_JU,'). \
                                replace(',LU,', ',bt_ch_state.state_LU,'). \
                                replace(',NE,', ',bt_ch_state.state_NE,'). \
                                replace(',NW,', ',bt_ch_state.state_NW,'). \
                                replace(',OW,', ',bt_ch_state.state_OW,'). \
                                replace(',SG,', ',bt_ch_state.state_SG,'). \
                                replace(',SH,', ',bt_ch_state.state_SH,'). \
                                replace(',SO,', ',bt_ch_state.state_SO,'). \
                                replace(',SZ,', ',bt_ch_state.state_SZ,'). \
                                replace(',TG,', ',bt_ch_state.state_TG,'). \
                                replace(',TI,', ',bt_ch_state.state_TI,'). \
                                replace(',UR,', ',bt_ch_state.state_UR,'). \
                                replace(',VD,', ',bt_ch_state.state_VD,'). \
                                replace(',VS,', ',bt_ch_state.state_VS,'). \
                                replace(',ZG,', ',bt_ch_state.state_ZG,'). \
                                replace(',ZH,', ',bt_ch_state.state_ZH,')
                            first_comma = new_line.find(',')
                            onrp = new_line[0:first_comma].replace('city_', '')
                            new_line = new_line + ',' + onrp
                            filewriter.writerow(new_line.split(','))
                            count_added += 1

            a = pd.read_csv('data/res.city.csv')
            b = pd.read_csv(newFileName, encoding='ISO-8859-1')
            c = pd.concat([a, b], axis=0)

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
