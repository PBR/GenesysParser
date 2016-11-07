#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Program entry point"""
from logger import *
from GenesysRequest import GenesysRequest


def main():
    log = logging.getLogger(__name__)
    log.info('Main start')
    genesysEntries = list()
    params = {'institute.code':
        [
            'NLD037',  # CGN: 165/165
            'USA003',  # Geneva: 2268/2639
            'DEU146',  # Gatersleben: 1603/1676
            'USA176',  # Tomato Genetics Resource Center: 260

            # 0 retrievals from Genesys:
            # 'USA093', 'USA094', 'USA645', 'USA646',  # Geneva: 0
            # 'USA647', 'USA648', 'USA649', 'USA167', 'USA168',  # Geneva: 0
            # 'DEU358', 'DEU416', 'DEU538'  # Gatersleben: 0
            # 'USA974',  # Geneva -> SSE: 26 -> 0 (parentheses issue)
            # Matched 4462/5679 accessions, i.e. 78.57%
        ],
        'taxonomy.genus': ['Solanum', 'Lycopersicon'],
        'taxonomy.species': ['lycopersicum', 'esculentum', 'sp.',
                             'pimpinellifolium', 'peruvianum'],
    }
    r = GenesysRequest(params)
    currPage = 1
    r.submitReq(page=currPage)
    genesysEntries += r.data
    log.info('Genesys request - total pages: %d' % r.totalPages)
    log.info('Genesys request - total elements: %d' % r.totalElements)
    counter = 0  # use for debugging
    while not r.last:
        currPage += 1
        log.info('Current page: %d' % currPage)
        r.submitReq(page=currPage)
        genesysEntries += r.data
        counter += 1
        if counter == 4: break  # use for debugging

    log.info('Retrieved ' + str(len(genesysEntries)) + '/' +
             str(r.totalElements) + ' elements from Genesys.')


if __name__ == '__main__':
    main()
