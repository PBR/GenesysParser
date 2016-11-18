#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
from datetime import datetime
import re
from logger import *


class ItemGenesys(object):
    """
        A single accession, as provided by Genesys. The Multicrop Passport
        Descriptor is used by the API, and is accessible as-is through the
        'item' class field.
        The most commonly used attributes are stored in separate fields,
        for ease of access and brevity. Theses are:
        [genesysUUID, acqDate, accessionID, collectionDate, genus, species,
        collSite, instituteCode, aliases].
    """

    log = logging.getLogger(__name__)

    def __init__(self, item):
        """
            Get MCPD dictionary. The fields to be extracted follow.
            :param item: dict
        """

        self.full = copy.deepcopy(item)

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
                                if x['type'] in ['ACCENAME', 'OTHERNUMB']
                                ])
            self.aliases = tuple(self.aliases)
        except TypeError:
            self.aliases = tuple()

    def __repr__(self):
        """
            Print the most commonly used attributes of the item.
            :return: string
        """
        temp_aliases = [self.cleanUnprintables(x) for x in self.aliases]
        if temp_aliases != self.aliases:
            self.encodingIssues = True
        return ('ItemGenesys(accessionID=%s, collectionDate=%s, ' +
                'otherNames=[%s], genus=%s, species=%s, instituteCode=%s, ' +
                'collectionSite=%s)') % \
               (self.accessionID, self.collectionDate,
                ', '.join(temp_aliases), self.genus, self.species,
                self.instituteCode, self.collectionSite)

    def __eq__(self, other):
        return self.accessionID == other.accessionID

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def __hash__(self):
        return hash(self.accessionID)
        # return hash(self.__repr__())

    @staticmethod
    def parseDate(tempDate):
        """
            Parse a Genesys date string and return it as a Date.
            Things to consider are zero values for months and days,
            or months/days represented as --. In these cases, a default
            date of '0101' is attributed.
            :param tempDate: string
            :return date: datetime.date
        """
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
        """
            Remove characters that the terminal cannot print.
            :param dirty: string
            :return: string
        """
        return re.sub('[^\s!-~]', '', dirty)
