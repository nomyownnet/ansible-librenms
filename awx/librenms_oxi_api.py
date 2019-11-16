#!/usr/bin/env python3

import json
import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://librenms.org/api/v0/oxidized'
headers = {'X-Auth-Token': 'token'}
req = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(req).read()
inventory = {}
hostvars = {}
meta = {'hostvars': hostvars}
for i in json.loads(response):
    if i['group'] not in inventory:
        inventory[i['group']] = {'hosts':[]}
        inventory[i['group']]['hosts'].append(i['hostname'])
    else:
        inventory[i['group']]['hosts'].append(i['hostname'])
    meta['hostvars'][i['hostname']] = {'ansible_host':i['ip'], 'os': i['os'], 'group_names': i['group']}
inventory['_meta'] = meta
print(json.dumps(inventory))
