#!/usr/bin/env python
import copy
from datetime import datetime
import re


class ItemGenesys(object):
    
    def __init__(self, item):
        """ Get dict. The fields to be extracted follow. """
        self.encodingIssues = False
        self.accessionID = item['acceNumb']
        self.parseDate(item['acqDate'])
        try:
            self.aliases = set([x['name'] for x in item['aliases']
                            if x['type'] == 'ACCENAME'])
            self.aliases = tuple(self.aliases)
        except:
            self.aliases = tuple()
            
        self.genus = item['taxonomy']['genus']
        self.species = item['taxonomy']['species']
        self.instituteCode = None
        self.collectionSite = None
        try:
            if 'coll' in item:
                self.collectionSite = item['coll']['collSite']
            if 'institute' in item:
                self.instituteCode = item['institute']['code']
        except (KeyError, TypeError):
            pass
            # todo
    
    
    def __repr__(self):
        temp_aliases = [self.cleanUnprintables(x) for x in self.aliases]
        if temp_aliases != self.aliases:
            self.encodingIssues = True
        return ('ItemGenesys(accessionID=%s, collectionDate=%s, ' + \
                'otherNames=[%s], genus=%s, species=%s, instituteCode=%s, ' + \
                'collectionSite=%s)') % \
               (self.accessionID, self.collectionDate,
                ', '.join(temp_aliases), self.genus, self.species, \
                self.instituteCode, self.collectionSite)


    def parseDate(self, tempDate):
        if tempDate is None:
            tempDate = '00010101'
        elif tempDate[4:6] in ['00', '--']:
            tempDate = tempDate[:4] + '0101'
        elif tempDate[-2:] in ['00', '--']:
            tempDate = tempDate[:6] + '01'
        self.collectionDate =  datetime.strptime(tempDate, '%Y%m%d').date()
        
    @staticmethod
    def cleanUnprintables(dirty):
        return re.sub('[^\s!-~]', '', dirty)
