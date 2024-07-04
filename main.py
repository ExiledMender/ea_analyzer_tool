import subprocess
import sys
import os
import json

from info_to_json import slice_json
from testconnection_to_json import convert_test_connection_to_json
from create_html import generate_html_from_json

def main():
    python_executable = sys.executable
    script_path = os.path.join(os.path.dirname(__file__), "select_directory.py")
    subprocess.run([python_executable, script_path])

    root_path = os.path.dirname(os.path.abspath(__file__))
    info_txt_path = os.path.join(root_path, "temp", "Info.txt")
    info_json_path = os.path.join(root_path, "temp", "json", "Info.json")
    test_connections_path = os.path.join(root_path, "temp", "TestConnections.txt")
    test_connection_output = os.path.join(root_path, "temp", "json", "TestConnections.json")
    machine_info_path = os.path.join(root_path, "temp", "machine_info.json")

    logs_dir = os.path.join(root_path, "temp")
    analyzer_dir = os.path.join(logs_dir, "json")
    os.makedirs(analyzer_dir, exist_ok=True)

    # Save info.json
    info_json_data = slice_json(info_txt_path)
    if info_json_data is not None:
        os.makedirs(os.path.dirname(info_json_path), exist_ok=True)
        with open(info_json_path, "w") as a_info:
            json.dump(info_json_data, a_info, indent=4)
        print(f"Parsed {info_txt_path} and successfully created {test_connection_output}")
    else:
        print("Failed to analyze 'info.txt.'")

    test_values = convert_test_connection_to_json(test_connections_path, test_connection_output)
    if test_values is not None:
        print(f"Parsed {test_connections_path} and successfully created {test_connection_output}")
    else:
        print("Failed to analyze 'TestConnections.txt'")

    html_output_path = os.path.join("results", "AnalyzerResults.html")
    generate_html_from_json(info_json_path, html_output_path)
    print(f"HTML report generated at {html_output_path}")

    files_to_delete = [
        info_txt_path,
        info_json_path,
        test_connections_path,
        test_connection_output,
        machine_info_path
    ]

    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted {file_path}")
        except FileNotFoundError:
            print(f"{file_path} not found, skipping deletion.")

if __name__ == "__main__":
    main()