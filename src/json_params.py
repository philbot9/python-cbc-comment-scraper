import json

default_json_params = {
    'limit': 100,
    'child_limit': 100,
    'sort': 'oldest',
    'section': '2.632',
    'verb': 'get'
}


def build_params(params, after_id = ''):
    request_params = {
        **default_json_params,
        **params
    }

    if after_id != '':
        request_params['after_id'] = after_id

    return request_params


def build_json_data(request_num, request_params):
    return {
        'site': 'www.cbc.ca',
        'requests': {
            request_num: request_params
        }
    }


def build_page_params(page_id, request_num, params, after_id =''):
    request_params = build_params(params, after_id)
    request_params['route'] = f'/pages/{page_id}/threads'
    json_data = build_json_data(request_num, request_params)

    return json.dumps(json_data)


def build_thread_params(thread_id, request_num, params, after_id =''):
    request_params = build_params(params, after_id)
    request_params['route'] = f'/threads/${thread_id}/comments'
    json_data = build_json_data(request_num, request_params)

    return json.dumps(json_data)
