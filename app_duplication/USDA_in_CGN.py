#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from logger import *
from fetch_data import *


def USDA_in_CGN(verbosity=True):
    log = logging.getLogger(__name__)
    log.info('Start.')
    # UDSA accession name pattern: PI + 6 digits, space optional
    pat_pi = re.compile(u'PI ?\d{6}\D?')
    pat_inst = re.compile(u'USA\d{3}\D?')

    # read Json into Genesys items
    r = GenesysParser()
    cgn_items = r.readFromJson('CGN.txt')

    dupl_pi_pattern = set()
    dupl_usa_pattern = set()
    dupl_instcode_search = set()
    dupl_instcode_official = set()
    dupl_instcode_all = set()

    for i in cgn_items:
        for alias in i.full['aliases']:
            # check if alias name adheres to PI pattern
            pi_matches = re.findall(pat_pi, alias['name'])
            if pi_matches:
                dupl_pi_pattern.add(i)

            if alias['usedBy']:  # filter out None's

                if alias['usedBy'] in usda_institutions_fromSearch:
                    dupl_instcode_search.add(i)
                if alias['usedBy'] in usda_institutions_official:
                    dupl_instcode_official.add(i)
                if alias['usedBy'] in usda_all:
                    dupl_instcode_all.add(i)

                inst_matches = re.findall(pat_inst, alias['usedBy'])
                if inst_matches:
                    dupl_usa_pattern.add(i)

    printL(dupl_instcode_official, 'Items in official USDA list', verbosity)  # 26
    printL(dupl_instcode_search, 'Items in searchable USDA institutions', verbosity)  # 52
    printL(dupl_pi_pattern, 'Items with PI pattern', verbosity)  # 54
    printL(dupl_instcode_all, 'Items in combined official and searchable UDSA lists', verbosity)  # 69
    printL(dupl_usa_pattern, 'Items with USA pattern', verbosity)  # 75

    printL(dupl_instcode_official - dupl_instcode_search, 'official - searchable', verbosity)  # 17
    printL(dupl_instcode_search - dupl_instcode_official, 'searchable - official', verbosity)  # 43
    printL(dupl_pi_pattern - dupl_usa_pattern, 'pi pattern - usa pattern', verbosity)  # 1
    printL(dupl_usa_pattern - dupl_pi_pattern, 'usa pattern - pi pattern', verbosity)  # 22
    printL(dupl_pi_pattern | dupl_usa_pattern, 'pi pattern v usa pattern', verbosity)  # 76

    printL(dupl_instcode_official | dupl_instcode_search | dupl_pi_pattern | \
           dupl_instcode_all | dupl_usa_pattern, 'all union', verbosity)  # 76
    printL(dupl_instcode_official & dupl_instcode_search & dupl_pi_pattern & \
           dupl_instcode_all & dupl_usa_pattern, 'all intersection', verbosity)  # 9


if __name__ == '__main__':
    fetch_data()
    USDA_in_CGN(verbosity=False)
    print('Done.')
