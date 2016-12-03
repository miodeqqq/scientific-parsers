#! /usr/bin/env python

# -*- coding: utf-8 -*-

class Colors():
    """
    Class defines colors to be used in console prints.
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


urls_dict = {
    'grobid': 'http://localhost:1234/processFulltextDocument',
    'tika': 'http://localhost:9876/tika',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}