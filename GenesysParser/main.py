#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
from logger import *
from GenesysParser import GenesysParser


def main():
    """
        Example use of GenesysRequest
    """
    log = logging.getLogger(__name__)
    log.info('Main start')
    # Setting the query parameters
    query_params = \
        {
            'institute.code':
                [
                    'NLD037',  # CGN
                    'USA003',  # Geneva
                    'DEU146',  # Gatersleben
                    'USA176',  # Tomato Genetics Resource Center
                ],
                'taxonomy.genus': ['Solanum', 'Lycopersicon'],
                'taxonomy.species': ['lycopersicum', 'esculentum', 'sp.',
                                     'pimpinellifolium', 'peruvianum'],
        }
    genesysEntries = list()
    r = GenesysParser(query_params)

    # example: fetching pages one by one
    fetch_one_by_one = True
    if fetch_one_by_one:
        currPage = 1
        while not r.last:
            log.info('Current page: %d' % currPage)
            r.submitReq(page=currPage)
            genesysEntries += copy.deepcopy(r.results)
            if currPage == 4: break  # use only for debugging
            currPage += 1
            # Fetch only 3 out of 333 pages!
            if currPage == 4: break

    # example: fetching all pages at once
    fetch_all_at_once = False
    if fetch_all_at_once:
        # WARNING: many pages!
        genesysEntries = r.fetchAll()

    for result_item in genesysEntries:
        print(result_item)
        print(result_item.full['acceNumb'])

    log.info('Retrieved ' + str(len(genesysEntries)) + '/' +
             str(r.totalElements) + ' elements from Genesys.')


if __name__ == '__main__':
    """
        Program entry point
    """
    main()
