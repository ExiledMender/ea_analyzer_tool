import subprocess
import sys
import os
import json
import shutil
import argparse

from info_to_json import slice_json
from testconnection_to_json import convert_test_connection_to_json
from create_html import generate_html_from_json

def open_directory(path):
    if sys.platform == 'win32':
        os.startfile(path)
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', path])
    else:
        subprocess.Popen(['xdg-open', path])

def main():
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument('--debug', action='store_true', help="Enable debug output")
    args = parser.parse_args()

    debug = args.debug

    python_executable = sys.executable
    script_path = os.path.join(os.path.dirname(__file__), "select_directory.py")
    subprocess.run([python_executable, script_path] + (["--debug"] if debug else []))

    root_path = os.path.dirname(os.path.abspath(__file__))
    info_txt_path = os.path.join(root_path, "temp", "Info.txt")
    info_json_path = os.path.join(root_path, "temp", "json", "Info.json")
    test_connections_path = os.path.join(root_path, "temp", "TestConnections.txt")
    test_connection_output = os.path.join(root_path, "temp", "json", "TestConnections.json")
    machine_info_path = os.path.join(root_path, "temp", "machine_info.json")
    system_info_path = os.path.join(root_path, "temp", "SystemInfo.json")
    system_info_output = os.path.join(root_path, "temp", "json", "SystemInfo.json")
    services_info_path = os.path.join(root_path, "temp", "Services.json")
    services_info_output = os.path.join(root_path, "temp", "json", "Services.json")
    runningprocesses_info_path = os.path.join(root_path, "temp", "RunningProcesses.json")
    runningprocesses_info_output = os.path.join(root_path, "temp", "json", "RunningProcesses.json")

    logs_dir = os.path.join(root_path, "temp")
    analyzer_dir = os.path.join(logs_dir, "json")
    os.makedirs(analyzer_dir, exist_ok=True)

    info_json_data = slice_json(info_txt_path)
    if info_json_data is not None:
        os.makedirs(os.path.dirname(info_json_path), exist_ok=True)
        with open(info_json_path, "w") as a_info:
            json.dump(info_json_data, a_info, indent=4)
        if debug:
            print(f"Parsed {info_txt_path} and successfully created {info_json_path}")
    else:
        print("Failed to analyze 'Info.txt.'")

    test_values = convert_test_connection_to_json(test_connections_path, test_connection_output)
    if test_values is not None:
        if debug:
            print(f"Parsed {test_connections_path} and successfully created {test_connection_output}")
    else:
        print("Failed to analyze 'TestConnections.txt'")

    if os.path.exists(system_info_path):
        shutil.copy(system_info_path, system_info_output)
        if debug:
            print(f"Copied {system_info_path} to {system_info_output}")
    else:
        print(f"SystemInfo.json not found at {system_info_path}")

    if os.path.exists(services_info_path):
        shutil.copy(services_info_path, services_info_output)
        if debug:
            print(f"Copied {services_info_path} to {services_info_output}")
    else:
        print(f"Services.json not found at {services_info_path}")

    if os.path.exists(runningprocesses_info_path):
        shutil.copy(runningprocesses_info_path, runningprocesses_info_output)
        if debug:
            print(f"Copied {runningprocesses_info_path} to {runningprocesses_info_output}")
    else:
        print(f"RunningProcesses.json not found at {runningprocesses_info_path}")

    html_output_path = os.path.join("results", "Analyzer_Results.html")
    host_name, html_path_with_name = generate_html_from_json(info_json_path, html_output_path)
    print(f"HTML report generated at {html_path_with_name} for host {host_name}")

    # Open the directory where the HTML file was created
    open_directory(os.path.dirname(html_path_with_name))

    files_to_delete = [
        info_txt_path,
        info_json_path,
        test_connections_path,
        test_connection_output,
        machine_info_path,
        system_info_path,
        system_info_output,
        services_info_path,
        services_info_output,
        runningprocesses_info_path,
        runningprocesses_info_output
    ]

    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            if debug:
                print(f"Deleted {file_path}")
        except FileNotFoundError:
            if debug:
                print(f"{file_path} not found, skipping deletion.")

if __name__ == "__main__":
    main()
