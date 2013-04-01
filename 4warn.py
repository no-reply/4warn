#!/usr/bin/env python

import sys
import time
import json
import urllib2

class Thread:
    def __init__(self, board, no, json=None):
        self.board = board
        self.no = no
        self.json = json
        self.updated = None

    def update(self):
        url = 'http://api.4chan.org/'+ self.board + '/res/' + str(self.no) + '.json'
        req = urllib2.Request(url)
        if self.updated:
            req.add_header("If-Modified-Since", self.updated)
        handle = urllib2.urlopen(req)
        if handle.code == 200:
            self.json = json.loads(handle.read())
            headers = handle.info()
            self.updated = headers.getheader("Last-Modified")
            # let's follow the api rules and wait 1 after each request
            time.sleep(1)

    def search(self, q):
        self.update()
        results = []
        for post in self.json['posts']:
            if 'com' in post:
                if q.lower() in post['com'].lower():
                    results.append(post['com'])
        return results

def threads(board):
    """given a board, return a list of threads on the board.
       for some reason fourch doesn't support this request.
    """
    threads = []
    url = 'http://api.4chan.org/'+ board + '/threads.json'
    response = json.loads(urllib2.urlopen(url).read())
    # let's follow the api rules and wait 1 after each request
    time.sleep(1)
    for page in response:
        for thread in page['threads']:
            threads.append(Thread(board, thread['no']))
        
    return threads

if __name__ == "__main__":
    b = sys.argv[1]
    q = sys.argv[2]

    for thread in threads(b):
        hits = thread.search(q)
        if len(hits) > 0:
            for hit in hits:
                print hit

    
