import api
import json
import sqlite3
import time
import sys
from collections import deque


optimization_set = set()
def process_matches(matches):
    for match in matches:
        if match[u'lobby_type'] == 0 and len(match[u'players']) == 10 and match[u'match_id'] not in optimization_set:
            cur.execute('insert or ignore into matches (match_id, json) values (?, ?)',
                       (match[u'match_id'], json.dumps(match)))
            conn.commit()
            optimization_set.add(match[u'match_id'])
def get_nmatches():
    cur.execute('select count(*) from matches')
    return cur.fetchone()[0]
def init():
    matches = api.get_match_history(min_players=10)[u'matches']
    requests_done = 1
    while matches:
        requests_done += 1
        process_matches(matches)
        next_matches = min(match[u'match_id'] for match in matches)
        matches = api.get_match_history(min_players=10,
                                        start_at_match_id=next_matches + 1)[u'matches']
    #time.sleep(requests_done * 1.25)
conn = sqlite3.connect('matches.db')
cur = conn.cursor()

sleep_time = 5

matches_q = deque()
matches_total = get_nmatches()
cur_time = time.time()

for i in xrange(0, 60, sleep_time):
    matches_q.append((matches_total, cur_time))
#try:
#    init()
#except Exception as e:
#    print e
    
while True:
    try:
        #process_matches(api.get_match_history(min_players=10, matches_requested=100)[u'matches'])
        init()
        matches_total = get_nmatches()
        matches_prev, prev_time = matches_q.popleft()
        cur_time = time.time()
        matches_per_minute = int(round((matches_total - matches_prev) / (cur_time - prev_time) * 60))
        matches_q.append((matches_total, cur_time))
        sys.stdout.write('\r'+ time.strftime('%H:%M:%S') + ' ' + str(matches_total) + ' ' + str(matches_per_minute))
        sys.stdout.flush()
    except Exception as e:
        print e
    time.sleep(sleep_time)
