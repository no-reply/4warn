#!/usr/bin/env python

import sys
import time
import json
import urllib2
import fourch

def threads(board):
    """return a list of threads on the board.
       for some reason fourch doesn't support this request.
    """
    threads = []
    url = 'http://api.4chan.org/'+ board.name + '/threads.json'
    response = json.loads(urllib2.urlopen(url).read())
    for page in response:
        for thread in page['threads']:
            threads.append(fourch.thread(board, thread['no']))
        
    return threads

if __name__ == "__main__":
    b = fourch.board(sys.argv[1])
    q = sys.argv[2]

    print threads(b)
    
