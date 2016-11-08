#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import copy
from .ItemGenesys import ItemGenesys
from .logger import *
from . import config


class GenesysParser(object):
    """
        A class responsible for defining and submitting a query to the
        Genesys API, and then fetching the results.
    """
    log = logging.getLogger(__name__)

    def __init__(self, cFilter):
        """
            Instantiate a GenesysRequest with the desired query parameters.
            :param cFilter: dict
            :param page: int
            :param size: int
        """
        GenesysParser.log.warning('genesys')
        self.body = {'filter': json.dumps(cFilter)}
        self.url = (config.url + ('/' if config.url[-1] != '/' else '') +
                    'webapi/v0/acn/filter?client_id=' +
                    config.clientID + '&client_secret=' + config.clientSecret)

        self.headers = {'Content-Type': 'application/json',
                        'Referer': 'http://ecpgr.cgn.wur.nl/eupotato/test.html'}
        self.totalElements = 0
        self.totalPages = 0
        self.last = False
        self.results = list()

    def submitReq(self, page=None, size=None):
        """
            Query Genesys for a specific page, with a specified number of
            results (cannot exceed 50 results per page).
            :param page: int
            :param size: int
            :return: list(ItemGenesys)
        """
        if page is not None:
            self.body['startAt'] = page if page < 0 else 1
        else:
            page = 1
        if size is not None:
            # up to 50 records/page:
            self.body['maxRecords'] = size if 0 < size < 51 else 50
        else:
            size = 50
        response = requests.post(self.url, json=self.body, headers=self.headers)
        response = json.loads(response.text)
        entries = list()
        try:
            self.totalElements = response['totalElements']
            self.totalPages = response['totalPages']
            entries = copy.deepcopy(response['content'])
            self.results = [ItemGenesys(x) for x in entries]
            self.last = response['last']
            GenesysParser.log.info('Genesys request - total pages: %d' %
                                    self.totalPages)
            GenesysParser.log.info('Genesys request - total elements: %d' %
                                    self.totalElements)
        except KeyError:
            GenesysParser.log.warning('No results.')
            self.totalElements, self.totalPages, self.results = 0, 0, list()
        return self.results

    def fetchAll(self):
        """
            Get the full result for a query. This means that all pages are
            fetched, as opposed to the submitReq() function that only receives
            the page specified.
            :return results: list(ItemGenesys)
        """
        entries = copy.deepcopy(self.submitReq(page=1))
        currentPage = 2
        GenesysParser.log.info('Genesys request - total pages: %d' % \
                                self.totalPages)
        GenesysParser.log.info('Genesys request - total elements: %d' % \
                                self.totalElements)
        self.last = False
        while not self.last:
            GenesysParser.log.info('Current page: %d' % currentPage)
            entries += copy.deepcopy(self.submitReq(page=currentPage))
            currentPage += 1
            # break  # use for debugging
        self.results = copy.deepcopy(entries)
        return self.results


if __name__ == '__main__':
    # params = {'acceNumb': ['PI 340908']}
    params = {'crop': ['tomato']}
    if 0:
        a = GenesysParser(params)
        # Fetch page 1 and limit to 10 results
        a.submitReq(size=10, page=1)
        for item in a.results:
            GenesysParser.log.debug(item)

    if 1:
        a = GenesysParser(params)
        for x in a.fetchAll():
            print(x)
        print(len(a.results))

