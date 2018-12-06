import requests
import flask
import secrets as s

debug = 1

channels = [s.c[0], s.c[1], s.c[2], s.c[3]]
channels = [str(channel) for channel in channels]

req_urls = ['https://thingspeak.com/channels/' + channel + '/feed.json' for channel in channels]

if debug:
    print(req_urls)

req_results = [requests.get(url) for url in req_urls]

if debug:
    for i in range(len(req_results)):
        print(req_results[i].status_code)
