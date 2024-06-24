# main.py
import json
import os

from info_to_json import slice_json
from testconnection_to_json import convert_test_connection_to_json

def main():
    # Set up paths for info.txt conversion
    root_path = os.path.dirname(os.path.abspath(__file__))
    info_txt_path = os.path.join(root_path, "logs/info.txt")
    info_json_data = slice_json(info_txt_path)

    # Save info.json
    with open(os.path.join(root_path, "logs", "analyzer/info.json"), "w") as a_info:
        json.dump(info_json_data, a_info, indent=4)
    print("info.txt has been analyzed and converted.")
    
    # Set up paths for TestConnection.txt conversion
    test_connections_path = os.path.join(root_path, "logs/TestConnections.txt")
    test_connection_output = os.path.join(root_path, "logs/analyzer/TestConnections.json")    

    # Convert TestConnections.txt to JSON
    test_values = convert_test_connection_to_json(test_connections_path, test_connection_output)
    if test_values is not None:
        print("TestConnections.txt has been analyzed and converted to TestConnections.json.")

if __name__ == "__main__":
    main()