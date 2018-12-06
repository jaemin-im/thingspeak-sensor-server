from pandas.io.json import json_normalize

import pandas as pd
import requests
import json

import secrets as s


def main(debug):
    channels = [s.c[0], s.c[1], s.c[2], s.c[3]]
    channels = [str(channel) for channel in channels if channel is not None]

    temp_req_urls = ['https://thingspeak.com/channels/' + channel + '/fields/1.json' for channel in channels if channel is not None]
    humid_req_urls = ['https://thingspeak.com/channels/' + channel + '/fields/2.json' for channel in channels if channel is not None]

    if debug:
        print(temp_req_urls)
        print(humid_req_urls)

    temp_req_results_raw = [requests.get(url) for url in temp_req_urls]
    humid_req_results_raw = [requests.get(url) for url in humid_req_urls]

    if debug:
        for t_result in temp_req_results_raw:
            print(t_result.status_code)
        for h_result in humid_req_results_raw:
            print(h_result.status_code)

    temp_req_results = [json.loads(result.text) for result in temp_req_results_raw]
    humid_req_results = [json.loads(result.text) for result in humid_req_results_raw]

    if debug:
        temp_df = [pd.DataFrame.from_dict(res['feeds']).dropna() for res in temp_req_results]
        humid_df = [pd.DataFrame.from_dict(res['feeds']).dropna() for res in humid_req_results]

        print(temp_df[0])
        print(humid_df[0])

    print('=== Mission Complete! ===')


if __name__ == '__main__':
    main(debug=True)