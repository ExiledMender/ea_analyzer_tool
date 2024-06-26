import subprocess
import sys
import os
import json

from info_to_json import slice_json
from testconnection_to_json import convert_test_connection_to_json
from create_html import generate_html_from_json

def main():
    python_executable = sys.executable
    script_path = os.path.join(os.path.dirname(__file__), "lazy.py")
    subprocess.run([python_executable, script_path])

    # Continue with the rest of main.py logic
    root_path = os.path.dirname(os.path.abspath(__file__))
    info_txt_path = os.path.join(root_path, "logs", "info.txt")
    info_json_path = os.path.join(root_path, "logs", "Analyzer", "Info.json")
    test_connections_path = os.path.join(root_path, "logs", "TestConnections.txt")
    test_connection_output = os.path.join(root_path, "logs", "Analyzer", "TestConnections.json")
    machine_info_path = os.path.join(root_path, "logs", "machine_info.json")  # Add machine_info.json path

    # Ensure the output directories exist
    logs_dir = os.path.join(root_path, "logs")
    analyzer_dir = os.path.join(logs_dir, "Analyzer")
    os.makedirs(analyzer_dir, exist_ok=True)

    # Save info.json
    info_json_data = slice_json(info_txt_path)
    if info_json_data is not None:
        os.makedirs(os.path.dirname(info_json_path), exist_ok=True)
        with open(info_json_path, "w") as a_info:
            json.dump(info_json_data, a_info, indent=4)
        print("'Info.json' created successfully.")
    else:
        print("Failed to analyze 'info.txt.'")

    # Convert TestConnections.txt to JSON
    test_values = convert_test_connection_to_json(test_connections_path, test_connection_output)
    if test_values is not None:
        print("'TestConnections.json' created successfully.")
    else:
        print("Failed to analyze 'TestConnections.txt'")

    # Generate HTML report
    html_output_path = os.path.join(analyzer_dir, "AnalyzerResults.html")
    generate_html_from_json(info_json_path, html_output_path)
    print(f"HTML report generated at '{html_output_path}'")

    # Delete files
    files_to_delete = [
        info_txt_path,
        info_json_path,
        test_connections_path,
        test_connection_output,
        machine_info_path  # Add machine_info.json to the list
    ]

    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted {file_path}")
        except FileNotFoundError:
            print(f"{file_path} not found, skipping deletion.")

if __name__ == "__main__":
    main()