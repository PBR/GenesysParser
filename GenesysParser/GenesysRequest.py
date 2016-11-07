#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import json
import requests
import copy
from ItemGenesys import ItemGenesys
from logger import *


class GenesysRequest(object):
    log = logging.getLogger(__name__)

    def __init__(self, cFilter, page=1, size=50):
        GenesysRequest.log.warning('genesys')
        self.body = {'filter': json.dumps(cFilter),
                     'startAt': page if page < 0 else 1,
                     # up to 50 records/page:
                     'maxRecords': size if 0 < size < 51 else 50}
        self.url = (config.url + ('/' if config.url[-1] != '/' else '') +
                    'webapi/v0/acn/filter?client_id=' +
                    config.clientID + '&client_secret=' + config.clientSecret)

        self.headers = {'Content-Type': 'application/json',
                        'Referer': 'http://ecpgr.cgn.wur.nl/eupotato/test.html'}
        self.data = list()
        self.totalElements = 0
        self.totalPages = 0
        self.last = False

    def submitReq(self, page=None, size=None):
        if page is not None:
            self.body['startAt'] = page
        if size is not None:
            self.body['maxRecords'] = size
        response = requests.post(self.url, json=self.body, headers=self.headers)
        response = json.loads(response.text)
        entries = list()
        try:
            self.totalElements = response['totalElements']
            self.totalPages = response['totalPages']
            entries = copy.deepcopy(response['content'])
            self.data = [ItemGenesys(x) for x in entries]
            self.last = response['last']
        except KeyError:
            GenesysRequest.log.warning('No results.')
            self.totalElements, self.totalPages, self.data = 0, 0, list()
        return entries


if __name__ == '__main__':
    params = {'acceNumb': ['PI 340908']}
    params = {'crop': ['tomato']}
    a = GenesysRequest(params)
    a.submitReq(size=10, page=1)
    for item in a.data:
        ItemGenesys.log.debug(item)
        if item.encodingIssues:
            GenesysRequest.log.warning('Encoding issue for item with ' +
                                       item.accessionID)
