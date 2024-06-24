# main.py
import json
import os

from info_to_json import slice_json

def main():
    root_path = os.path.dirname(os.path.abspath(__file__))
    info_txt_path = os.path.join(root_path, "logs/info.txt")
    json_data = slice_json(info_txt_path)
    with open(os.path.join(root_path, "logs", "analyzer/info.json"), "w") as a_info:
        json.dump(json_data, a_info, indent=4)
if __name__ == "__main__":
    main()