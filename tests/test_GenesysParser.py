#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import mock
from context import GenesysParser, ItemGenesys
import json


# This method will be used by the mock to replace requests.get
def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, text='{}', status=0):
            self.text = text
            self.status_code = status

    # url in args[0]
    # todo: verify request url
    if True:
        with open('./MCPD_Genesys_example.json') as json_data:
            resp_data = json_data.read()
        return MockResponse(resp_data, 200)

    else:
        return MockResponse('{}', 400)


class GenesysParserTest(unittest.TestCase):
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_submitReq(self, mock_post):
        with open('./MCPD_Genesys_example.json') as json_data:
            resp_data = json.load(json_data)
            goldResults = [ItemGenesys(x) for x in resp_data['content']]

        params = {'acceNumb': ['PI 100697']}
        r = GenesysParser(params)
        mockResults = r.submitReq()

        self.assertEqual(r.status, 200)
        self.assertTrue(len(mockResults) == len(goldResults))
        for actual, fake in zip(mockResults, goldResults):
            self.assertTrue(actual == fake)


