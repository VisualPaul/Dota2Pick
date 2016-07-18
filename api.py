import json
import urllib2
import numbers
API_KEY = 'B94614CB91ADABD7262ACA91F920C8E6'
app_id=570

def call_api_function(iface_name, method_name, version, appid = 570, **kwargs):
    url = ['https://api.steampowered.com/{iname}/{mname}/{ver}/?'.format(
        iname=iface_name,
        mname=method_name,
        ver=version
    )]
    url.append('appid={}'.format(appid))
    url.append('key=' + API_KEY)
    url.append('format=json')
    for key in kwargs:
        if kwargs[key] is not None:
            url.append('{}={}'.format(key, kwargs[key]))
    f = urllib2.urlopen('&'.join(url)) # NO WITH FOR YOU
    res = json.load(f)
    f.close()
    return res

def get_match_history(**kwargs):
    return call_api_function('IDOTA2Match_570', 'GetMatchHistory', 'v1',
                             **kwargs)[u'result']

def get_latest_matches(n_matches):
    matches_left = n_matches
    if matches_left == 0:
        return
    matches = get_match_history(min_players=10)[u'matches']
    next_matches = min(match[u'match_id'] for match in matches)
    matches.reverse()
    while matches_left != 0:
        if not matches:
            matches = get_match_history(min_players=10,
                                        start_at_match_id=next_matches + 1)[u'matches']
            matches.reverse()
            next_matches = min(match[u'match_id']
                                          for match in matches)        
        if matches[-1][u'lobby_type'] == 0:
            yield matches[-1];
            matches_left -= 1
        matches.pop()
