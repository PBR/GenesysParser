#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from logger import *
from fetch_data import *


def USDA_in_CGN():
    log = logging.getLogger(__name__)
    log.info('Start.')
    # CGN accession name pattern: CGN + 5 digits, no space
    pat_cgn = re.compile(u'CGN\d{5}\D?')

    # read Json into Genesys items
    r = GenesysParser()
    usda_items = r.readFromJson('USDA.txt')

    dupl_cgn_pattern = set()
    dupl_instcode = set()

    for i in usda_items:
        if i.full['aliases']:  #
            for alias in i.full['aliases']:
                # check if alias name adheres to CGN pattern
                cgn_matches = re.findall(pat_cgn, alias['name'])
                if cgn_matches:
                    dupl_cgn_pattern.add(i)

                if alias['usedBy']:  # filter out None's
                    if alias['usedBy'] == 'NLD037':
                        dupl_instcode.add(i)

    printL(dupl_cgn_pattern, 'Items with CGN pattern')  # 0
    printL(dupl_instcode, 'Items with aliases used by NLD037')  # 0

    # printL(dupl_cgn_pattern - dupl_instcode, 'CGN pattern v instcode')
    # printL(dupl_cgn_pattern - dupl_instcode, 'CGN pattern + instcode')
    # printL(dupl_cgn_pattern - dupl_instcode, 'CGN pattern - instcode')
    # printL(dupl_instcode - dupl_cgn_pattern, 'instcode - CGN pattern')


if __name__ == '__main__':
    fetch_data()
    USDA_in_CGN()
    print('Done.')
