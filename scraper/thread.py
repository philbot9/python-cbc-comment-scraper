import requests
from timestamp import now

from json_params import build_thread_params
from response import parse_response

request_num = 1


def fetch_thread(thread_id, params, after_id):
    timestamp = now()
    callback_param = f'Zepto{timestamp}'
    json_params = build_thread_params(thread_id, request_num, params, after_id)

    url_params = {
        'json': json_params,
        'callback': callback_param,
        '_': timestamp
    }

    http_response = requests.get('https://api.viafoura.co/v2/', params=url_params)
    response = parse_response(http_response.text, callback_param)

    return response['responses'][str(request_num)]['result']

