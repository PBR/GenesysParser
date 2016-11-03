#!/usr/bin/env python
import config
import json
import requests
import copy
from ItemGenesys import ItemGenesys


class GenesysRequest(object):
    
    def __init__(self, cFilter, page=1, size=50):
        self.body = {'filter': json.dumps(cFilter),
                     'startAt': page,
                     'maxRecords': size}  # up to 50 records/page
        self.url = config.url + '/webapi/v0/acn/filter?client_id=' + \
            config.clientID + '&client_secret=' + config.clientSecret
        self.headers = {'Content-Type': 'application/json',
                        'Referer': 'http://ecpgr.cgn.wur.nl/eupotato/test.html'}
        self.data = list()

    def submitReq(self, page=None, size=None):
        if page is not None:
            self.body['startAt'] = page
        if size is not None:
            self.body['maxRecords'] = size
        response = requests.post(self.url, json=self.body, headers=self.headers)
        response = json.loads(response.text)
        try:
            self.totalElements = response['totalElements']
            self.totalPages = response['totalPages']
            entries = copy.deepcopy(response['content'])
            self.data = [ItemGenesys(x) for x in entries]
            self.last = response['last']
            return entries
        except KeyError:
            print('No results.')
            self.totalElements, self.totalPages, self.data = 0, 0, []
            return []
    
    
if __name__ == '__main__':
    params = {'acceNumb': ['PI 340908']}
    a = GenesysRequest(params)
    a.submitReq(size=10, page=1)
    for item in a.data:
        print(item)
        if item.encodingIssues: print('issue')
            
