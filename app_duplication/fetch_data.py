#!/usr/bin/env python
# -*- coding: utf-8 -*-
from GenesysParser import GenesysParser
from logger import *
import os
import copy

# from official list: 30
# https://www.genesys-pgr.org/org/USDA
usda_institutions_official = [
    'USA003',
    'USA004',
    'USA016',
    'USA020',
    'USA022',
    'USA026',
    'USA028',
    'USA029',
    'USA033',
    'USA042',
    'USA047',
    'USA049',
    'USA074',
    'USA108',
    'USA129',
    'USA133',
    'USA134',
    'USA148',
    'USA151',
    'USA158',
    'USA167',
    'USA174',
    'USA176',
    'USA476',
    'USA955',
    'USA956',
    'USA962',
    'USA970',
    'USA971',
    'USA995'
]

# from full text search: 113
# https://www.genesys-pgr.org/1/acn/search2?section=institute&q=USDA
usda_institutions_fromSearch = [
    'CMR139',
    'PRI108',
    'PRI409',
    'UGA495',
    'USA003',
    'USA004',
    'USA005',
    'USA007',
    'USA016',
    'USA017',
    'USA020',
    'USA021',
    'USA022',
    'USA023',
    'USA026',
    'USA027',
    'USA028',
    'USA029',
    'USA030',
    'USA033',
    'USA039',
    'USA042',
    'USA044',
    'USA047',
    'USA049',
    'USA057',
    'USA081',
    'USA096',
    'USA097',
    'USA102',
    'USA104',
    'USA105',
    'USA108',
    'USA112',
    'USA120',
    'USA122',
    'USA123',
    'USA124',
    'USA125',
    'USA126',
    'USA127',
    'USA128',
    'USA129',
    'USA130',
    'USA131',
    'USA132',
    'USA133',
    'USA135',
    'USA136',
    'USA137',
    'USA138',
    'USA139',
    'USA140',
    'USA142',
    'USA143',
    'USA144',
    'USA145',
    'USA146',
    'USA147',
    'USA148',
    'USA149',
    'USA150',
    'USA151',
    'USA152',
    'USA153',
    'USA154',
    'USA155',
    'USA157',
    'USA158',
    'USA159',
    'USA160',
    'USA161',
    'USA163',
    'USA164',
    'USA166',
    'USA167',
    'USA169',
    'USA170',
    'USA174',
    'USA177',
    'USA178',
    'USA409',
    'USA412',
    'USA435',
    'USA436',
    'USA442',
    'USA469',
    'USA499',
    'USA514',
    'USA527',
    'USA551',
    'USA559',
    'USA570',
    'USA579',
    'USA605',
    'USA616',
    'USA623',
    'USA628',
    'USA639',
    'USA645',
    'USA647',
    'USA650',
    'USA652',
    'USA667',
    'USA702',
    'USA710',
    'USA740',
    'USA905',
    'USA937',
    'USA955',
    'USA962',
    'USA969',
    'USA972'
]

usda_all = list(set(copy.deepcopy(usda_institutions_fromSearch) + \
                    copy.deepcopy(usda_institutions_official)))

# Genesys only looks for tomato in the Solanaceae family.
# These can be retrieved from https://sandbox.genesys-pgr.org/api/v0/crops/tomato/rules?access_token=ACCESS_TOKEN
species = [
    'arcanum',
    'cheesmaniae',
    'chilense',
    'chmielewskii',
    'corneliomuelleri',
    'esculentum',
    'galapagense',
    'habrochaites',
    'habrochaites x lycopersicum',
    'hirsutum',
    'huaylasense',
    'juglandifolium',
    'lycopersicoides',
    'lycopersicon',
    'lycopersicum',
    'lycopersicum x chilense',
    'lycopersicum x habrochaites',
    'lycopersicum x lycopersicum',
    'lycopersicum x pennellii',
    'lycopersicum x pimpinellifolium',
    'neorickii',
    'ochranthum',
    'parvifolium',
    'pennellii',
    'peruvianum',
    'pimpinellifolium',
    'pimpinellifolium x lycopersicum',
    'rickii',
    'sitiens',
    # retrievable with {crops: tomato} from GCN, but not listed above:
    'lycopersicum x cheesmaniae',
    'corneliomulleri'
]


def fetch_data():
    """
        Fetch data from Genesys and save it into Json files.
        This data is used to study the duplication level between USDA and CGN.
    """
    log = logging.getLogger(__name__)
    log.info('Checking data files...')
    if not os.path.isfile('CGN.txt'):
        params_cgn = {
            'institute.code': ['NLD037'],
            # 'crops': ['tomato'],
            'taxonomy.genus': ['Solanum', 'Lycopersicon'],
            'taxonomy.species': species
        }
        cgn = GenesysParser(params_cgn)
        cgn.fetch2json('CGN.txt')
        log.info('CGN data has been saved.')
    else:
        log.info('CGN data file already exists.')

    if not os.path.isfile('USDA.txt'):
        params_usda = {
            'institute.code': usda_all,
            # 'crops': ['tomato'],
            'taxonomy.genus': ['Solanum', 'Lycopersicon'],
            'taxonomy.species': species
        }
        usda = GenesysParser(params_usda)
        usda.fetch2json('USDA.txt')
        log.info('USDA data has been saved.')
    else:
        log.info('USDA data file already exists.')


def printL(L, L_name='List', verbose=True):
    """
        Print a list. Start with the name, then iter through items.
        Finally print its length. Also works with sets, tuples...
    """
    if verbose:
        ('\n[' + L_name + ']:')
    if verbose:
        for item in list(L):
            print('\t' + str(item))
    print('[' + L_name + '] length: ' + str(len(L)) + '\n')


if __name__ == '__main__':
    fetch_data()
