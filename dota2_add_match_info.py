import sqlite3
import json
import api
import time
import sys

connection = sqlite3.connect('matches.db')
cur = connection.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS match_info (match_id INTEGER PRIMARY KEY, json)')
cur.execute('SELECT COUNT(*) FROM match_info')
cnt = cur.fetchone()[0]
cur.execute('SELECT COUNT(*) FROM matches')
total = cur.fetchone()[0]
sys.stdout.write('\r' + str(cnt))
sys.stdout.flush()

ins_cur = connection.cursor()
cur.execute('SELECT match_id FROM matches WHERE match_id NOT IN (SELECT match_id FROM match_info)')
for row in cur.fetchall():
    match_id = row[0]
    start_time = time.time()
    try:
        match = api.call_api_function('IDOTA2Match_570', 'GetMatchDetails', 'v1', match_id=match_id)
        ins_cur.execute('INSERT INTO match_info (match_id, json) VALUES (?, ?)',
                        (match_id, json.dumps(match)))
        connection.commit()
        cnt += 1
        sys.stdout.write('\r%d %d %.2f%%' % (cnt, total - cnt, float(cnt) / float(total) * 100))
        sys.stdout.flush()
    except Exception as e:
        print match_id, e
    time.sleep(max(0, 1. - (time.time() - start_time)))
