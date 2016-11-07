#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
from datetime import datetime
import re
from logger import *


class ItemGenesys(object):
    log = logging.getLogger(__name__)

    def __init__(self, item):
        """ Get dict. The fields to be extracted follow. """

        # The item field holds the entire MCPD as provided by Genesys.
        # The fields assigned to a separate class attribute are only the
        # ones that are used more commonly, for ease of access and brevity.
        self.item = copy.deepcopy(item)

        self.genesysUUID = item['uuid']
        self.acqDate = item['acqDate']
        self.accessionID = item['acceNumb']
        self.collectionDate = ItemGenesys.parseDate(item['acqDate'])
        self.genus = item['taxonomy']['genus']
        self.species = item['taxonomy']['species']

        self.encodingIssues = False
        try:
            if 'coll' in item:
                self.collectionSite = item['coll']['collSite']
        except (KeyError, TypeError):
            ItemGenesys.log.warning('Could not retrieve collection site for ' +
                                    self.accessionID)
            self.collectionSite = None
        try:
            if 'institute' in item:
                self.instituteCode = item['institute']['code']
        except (KeyError, TypeError):
            ItemGenesys.log.warning('Could not retrieve institute code for ' +
                                    self.accessionID)
            self.instituteCode = None

        try:
            self.aliases = set([x['name'] for x in item['aliases']
                                if x['type'] == 'ACCENAME'])
            self.aliases = tuple(self.aliases)
        except TypeError:
            self.aliases = tuple()

    def __repr__(self):
        temp_aliases = [self.cleanUnprintables(x) for x in self.aliases]
        if temp_aliases != self.aliases:
            self.encodingIssues = True
        return ('ItemGenesys(accessionID=%s, collectionDate=%s, ' +
                'otherNames=[%s], genus=%s, species=%s, instituteCode=%s, ' +
                'collectionSite=%s)') % \
               (self.accessionID, self.collectionDate,
                ', '.join(temp_aliases), self.genus, self.species,
                self.instituteCode, self.collectionSite)

    @staticmethod
    def parseDate(tempDate):
        """ Parse a Genesys date string and return it as a Date. """
        if tempDate is None:
            tempDate = '00010101'
        elif tempDate[4:6] in ['00', '--']:
            tempDate = tempDate[:4] + '0101'
        elif tempDate[-2:] in ['00', '--']:
            tempDate = tempDate[:6] + '01'
        date = datetime.strptime(tempDate, '%Y%m%d').date()
        return date

    @staticmethod
    def cleanUnprintables(dirty):
        return re.sub('[^\s!-~]', '', dirty)
