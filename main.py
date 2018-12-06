import datetime
import json

import pandas as pd
import requests
from flask import Flask

import secrets as s

app = Flask(__name__)


def data(debug):
    channels = [s.c[0], s.c[1], s.c[2], s.c[3]]
    channels = [str(channel) for channel in channels if channel is not None]

    temp_req_urls = ['https://thingspeak.com/channels/' + channel + '/fields/1.json' for channel in channels if
                     channel is not None]
    humid_req_urls = ['https://thingspeak.com/channels/' + channel + '/fields/2.json' for channel in channels if
                      channel is not None]

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

    temp_df_list = [pd.concat([(pd.DataFrame.from_dict(res['feeds']).dropna())['created_at'].map(
        lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=9)),
        (pd.DataFrame.from_dict(res['feeds']).dropna())['field1'].map(
            lambda x: x.rstrip('\r\n'))], axis=1) for res in temp_req_results]
    humid_df_list = [pd.concat([(pd.DataFrame.from_dict(res['feeds']).dropna())['created_at'].map(
        lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=9)),
        (pd.DataFrame.from_dict(res['feeds']).dropna())['field2'].map(
            lambda x: x.rstrip('\r\n'))], axis=1) for res in humid_req_results]

    if debug:
        print(temp_df_list[0])
        print(humid_df_list[0])
        print('=== Mission Complete! ===')

    test = {'td1': str(temp_df_list[0].iloc[-1, 0]), 'tv1': float(temp_df_list[0].iloc[-1, 1]),
            'hd1': str(humid_df_list[0].iloc[-1, 0]), 'hv1': float(humid_df_list[0].iloc[-1, 1]),
            'td2': str(temp_df_list[1].iloc[-1, 0]), 'tv2': float(temp_df_list[1].iloc[-1, 1]),
            'hd2': str(humid_df_list[1].iloc[-1, 0]), 'hv2': float(humid_df_list[1].iloc[-1, 1]),
            'td3': str(temp_df_list[2].iloc[-1, 0]), 'tv3': float(temp_df_list[2].iloc[-1, 1]),
            'hd3': str(humid_df_list[2].iloc[-1, 0]), 'hv3': float(humid_df_list[2].iloc[-1, 1]),
            'td4': str(temp_df_list[3].iloc[-1, 0]), 'tv4': float(temp_df_list[3].iloc[-1, 1]),
            'hd4': str(humid_df_list[3].iloc[-1, 0]), 'hv4': float(humid_df_list[3].iloc[-1, 1])
            }
    return test


@app.route('/data')
def return_data():
    return json.dumps(data(False))


if __name__ == '__main__':
    app.run(debug=True)
