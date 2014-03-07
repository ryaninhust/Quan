import sys
sys.path.append('/home/vagrant/personal/new_simi')

import requests

from core.models import session
from core.models.subjects import Location

COUNT = 100
loc_list_url = 'https://api.douban.com/v2/loc/list'

for start in range(0, 909, 100):
    play_load = {'count': COUNT, 'start': start}
    response = requests.get(loc_list_url, params=play_load)
    for loc in response.json()['locs']:
        location = Location()
        location.parent_uid = loc['parent']
        location.name = loc['name']
        location.loc_id = int(loc['id'])
        location.loc_uid = loc['uid']
        session.add(location)
        session.commit()
