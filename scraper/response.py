import re
import json


def parse_response(json_str, callback_param):
    clean_json_str = json_str.replace(callback_param, '')
    clean_json_str = re.sub(r"^\(", '', clean_json_str)
    clean_json_str = re.sub(r"\)$", '', clean_json_str)
    return json.loads(clean_json_str)
