# file_utils.py

import json
import os

def slice_json(info_txt_path):
    try:
        with open(info_txt_path, 'r') as df:
            data = df.read()
            start_position = data.find("Agent Info=")
            offset = len("Agent Info=")
            start_position = start_position + offset +1
            json_slice = data[start_position:]
            json_string = json.loads(json_slice)
            return json_string
    except IOError as e:
        print(f"Error reading file {info_txt_path}: {e}")
        return None
    except Exception as e:
        print(f"Error parsing file {info_txt_path}: {e}")
        return None