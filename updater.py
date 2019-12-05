#!/usr/bin/env python3
import requests
import json

default_api_url = "https://api.cloudflare.com/client/v4/zones/"

#CHANGE THIS
email = '<your email goes here>'
#the next 2 keys can be found in the overview tab of the dashboard
api_key = '<your api key goes here>'
zone_id = '<your zone id goes here'
#############

#First request - check if ip needs to be changed or not
ip = requests.get(url = 'http://checkip.amazonaws.com/').text.strip()

#Second request - get the ids of all the A records in your zone
headers = { 'X-Auth-Email' : email, 'X-Auth-Key' : api_key , 'Content-Type' : 'application/json' }
list_all_records_url = default_api_url + zone_id + "/dns_records?type=A"

r = requests.get(url = list_all_records_url, headers = headers)
all_records_response = r.json()

if 'success' not in all_records_response:
    exit()

if all_records_response['success'] == True:
    #invalid response from the server, no result found
    if 'result' not in all_records_response:
        exit()

    records = all_records_response['result']

    for record in records:
        if 'id' not in record or 'name' not in record:
            #invalid record format
            exit()

        update_dns_record_url = "{api_url}{zone_id}/dns_records/{record_id}".format(api_url = default_api_url, zone_id = zone_id, record_id = record['id'])

        record_data = { 'type' : 'A', 'name' : record['name'], 'content' : ip, 'proxied' : True }

        r = requests.put(url = update_dns_record_url, headers = headers, data = json.dumps(record_data))
