import json
import os

from info_to_json import slice_json
from testconnection_to_json import convert_test_connection_to_json
from create_html import generate_html_from_json

def main():
    # Set up paths for info.txt conversion
    root_path = os.path.dirname(os.path.abspath(__file__))
    info_txt_path = os.path.join(root_path, "logs/info.txt")
    info_json_data = slice_json(info_txt_path)

    # Ensure the output directory exists
    analyzer_dir = os.path.join(root_path, "logs", "Analyzer")
    os.makedirs(analyzer_dir, exist_ok=True)

    # Save info.json
    if info_json_data is not None:
        with open(os.path.join(analyzer_dir, "Info.json"), "w") as a_info:
            json.dump(info_json_data, a_info, indent=4)
        print("'Info.json' created successfully.")
    else:
        print("Failed to analyze 'info.txt.'")

    # Set up paths for TestConnection.txt conversion
    test_connections_path = os.path.join(root_path, "logs/TestConnections.txt")
    test_connection_output = os.path.join(analyzer_dir, "TestConnections.json")    

    # Convert TestConnections.txt to JSON
    test_values = convert_test_connection_to_json(test_connections_path, test_connection_output)
    if test_values is not None:
        print("'TestConnections.txt' created successfully.")
    else:
        print("Failed to analyze 'TestConnections.txt'")

    info_json_path = 'logs/Analyzer/Info.json'
    html_path = 'logs/Analyzer/AnalyzerResults.html'
    generate_html_from_json(info_json_path, html_path)


if __name__ == "__main__":
    main()