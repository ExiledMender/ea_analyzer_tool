import json
import os

def bytes_to_gb(bytes_value):
    return bytes_value / (1024 ** 3)

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error reading '{file_path}': {e}")
    return {}

def create_html_directory(html_path):
    html_dir = os.path.dirname(html_path)
    if html_dir:
        os.makedirs(html_dir, exist_ok=True)
    return html_dir

def get_drive_info(drives):
    storage_info_html = ''
    for drive in drives:
        total_size_gb = bytes_to_gb(drive.get('total_size', 0))
        freespace_available_gb = bytes_to_gb(drive.get('freespace_available', 0))
        storage_used_gb = total_size_gb - freespace_available_gb
        storage_used_percentage = (storage_used_gb / total_size_gb) * 100 if total_size_gb > 0 else 0
        storage_percentage_display = f"{storage_used_percentage:.2f}%"

        storage_info_html += f"""
        <div class="info-item">
            <label>Drive name:</label>
            <span>{drive.get('name', 'N/A')}</span>
        </div>
        <div class="info-item">
            <label>Volume label:</label>
            <span>{drive.get('volume_label', 'N/A')}</span>
        </div>
        <div class="info-item">
            <label>Drive format:</label>
            <span>{drive.get('drive_format', 'N/A')}</span>
        </div>
        <div class="info-item">
            <label>Storage:</label>
            <span>{storage_used_gb:.2f} GB of {total_size_gb:.2f} GB used ({storage_percentage_display})</span>
            <div class="storage-bar-container">
                <div class="storage-bar" style="width: {storage_used_percentage}%;"></div>
            </div>
            <br>
        </div>
        """
    return storage_info_html

def get_protection_info(plugins):
    protection_status = next((p.get('protection_status', {}) for p in plugins if p.get('product_name') == 'Endpoint Protection'), {})
    def get_indicator_symbol(status):
        return "✔" if status == "started" else "✖"

    protection_data = {
        'Malware Protection': protection_status.get('rtp', 'N/A'),
        'Exploit Protection': protection_status.get('ae', 'N/A'),
        'Behavior Protection': protection_status.get('arw', 'N/A'),
        'Web Protection': protection_status.get('mwac', 'N/A'),
        'Self Protection': protection_status.get('sp', 'N/A'),
    }
    protection_info_html = ""
    for key, value in protection_data.items():
        display_value = value.capitalize()
        indicator_symbol = get_indicator_symbol(value)
        protection_info_html += f"""
        <div class="info-item">
            <label>{key.title().replace('_', ' ')}:</label>
            <span class="indicator">{indicator_symbol}</span><span>{display_value}</span>
        </div>
        """
    return protection_info_html

def get_plugin_versions(plugins):
    plugin_version_map = {
        'Endpoint Protection': 'endpoint_protection',
        'Active Response Shell': 'active_response_shell',
        'Windows Remote Intrusion Detection and Prevention': 'brute_force_protection',
        'Asset Manager': 'asset_manager',
        'Endpoint Detection and Response': 'edr',
    }

    plugin_info = {key: next((p.get('plugin_version', 'N/A') for p in plugins if p.get('product_name') == key), 'N/A') for key in plugin_version_map}
    return plugin_info

def get_connection_results(connection_data):
    connection_results_html = ''
    def connection_indicator_symbol(status):
        return "✔" if status == "Passed" else "✖"

    for url, details in connection_data.items():
        status = "Passed" if details.get("Result", False) else "Failed"
        symbol = connection_indicator_symbol(status)
        connection_results_html += f'<div class="info-item-connection"><label>{url}</label><span class="indicator">{symbol}</span><span>{status}</span></div>\n'
    return connection_results_html

def generate_html_content(data, storage_info_html, protection_info_html, plugin_versions, connection_results_html):
    agent_info = data.get('AgentInfo', {})
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{agent_info.get('host_name', 'N/A')} Results</title>
        <style>
            body {{
                font-family: Consolas, monospace;
                padding: 20px;
            }}
            h1 {{
                margin-bottom: 20px;
            }}
            h3 {{
                margin-top: 40px;
            }}
            .info-item {{
                margin-bottom: 10px;
            }}
            .info-item label {{
                display: inline-block;
                width: 325px;
                font-weight: bold;
            }}
            .info-item-connection label {{
                display: inline-block;
                width: 670px;
                font-weight: bold;
                margin-bottom: 10px
            }}
            .indicator {{
                display: inline-block;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                margin-right: 10px;
            }}
            .indicator-started {{
                background-color: green;
            }}
            .indicator-stopped {{
                background-color: red;
            }}
            .left-column {{
                float: left;
                width: 50%;
            }}
            .right-column {{
                float: right;
                width: 50%;
            }}
            .full-width {{
                clear: both;
                width: 100%;
            }}
            .grey-background {{
                color: #808080;
                padding: 10px;
                margin-top: 20px;
            }}
            .grey-background a {{
                color: #808080;
                text-decoration: none;
                font-weight: bold;
            }}
            .grey-background a:hover {{
                text-decoration: underline;
            }}
            .storage-bar-container {{
                width: 90%;
                height: 10px;
                background-color: #f0f0f0;
                border-radius: 5px;
                margin-top: 5px;
                overflow: hidden;
            }}
            .storage-bar {{
                height: 100%;
                background-color: #4caf50;
            }}
        </style>
    </head>
    <body>
        <h1>Endpoint Agent Analyzer Results</h1>
        <div class="info-item">
            <label>Account Token:</label>
            <span>{data.get('AccountToken', 'N/A')}</span>
        </div>
        <div class="info-item">
            <label>Nebula Machine ID:</label>
            <span>{data.get('NebulaMachineId', 'N/A')}</span>
        </div>
        <hr>
        <div class="left-column">
            <h3>General Information</h3>
            <div class="info-item">
                <label>Endpoint Name:</label>
                <span>{agent_info.get('host_name', 'N/A')}</span>
            </div>
            <div class="info-item">
                <label>FQDN:</label>
                <span>{agent_info.get('fully_qualified_host_name', 'N/A')}</span>
            </div>
            <div class="info-item">
                <label>Last User:</label>
                <span>{agent_info.get('last_user', 'N/A')}</span>
            </div>
            <h3>Operating System</h3>
            <div class="info-item">
                <label>OS Version:</label>
                <span>{agent_info.get('os_info', {}).get('os_version', 'N/A')}</span>
            </div>
            <div class="info-item">
                <label>OS Friendly Name:</label>
                <span>{agent_info.get('os_info', {}).get('os_release_name', 'N/A')}</span>
            </div>
            <div class="info-item">
                <label>OS Type:</label>
                <span>{agent_info.get('os_info', {}).get('os_type', 'N/A')}</span>
            </div>
            <div class="info-item">
                <label>OS Architecture:</label>
                <span>{agent_info.get('os_info', {}).get('os_architecture', 'N/A')}</span>
            </div>
            <h3>Storage Information:</h3>
            {storage_info_html}
        </div>
        <div class="right-column">
            <h3>Protection Status</h3>
            {protection_info_html}
            <h3>Agent and Plugins</h3>
            <div class="info-item">
                <label>Endpoint Agent:</label>
                <span>{agent_info.get('engine_version', 'N/A')}</span>
            </div>
            <div class="info-item">
                <label>Endpoint Protection:</label>
                <span>{plugin_versions['Endpoint Protection']}</span>
            </div>
            <div class="info-item">
                <label>Active Response Shell:</label>
                <span>{plugin_versions['Active Response Shell']}</span>
            </div>
            <div class="info-item">
                <label>Brute Force Protection:</label>
                <span>{plugin_versions['Windows Remote Intrusion Detection and Prevention']}</span>
            </div>
            <div class="info-item">
                <label>Asset Manager:</label>
                <span>{plugin_versions['Asset Manager']}</span>
            </div>
            <div class="info-item">
                <label>Endpoint Detection and Response:</label>
                <span>{plugin_versions['Endpoint Detection and Response']}</span>
            </div>
        </div>
        <div class="full-width">
            <hr>
            <h3>Connection Test Results</h3>
            {connection_results_html}
        </div>
        <div class="full-width grey-background">
            * If one of the above failed, ask the customer to review:
            <a href="https://support.threatdown.com/hc/en-us/articles/4413798711699-Network-access-requirements-for-Nebula">Network access requirements for Nebula</a>
        </div>
    </body>
    </html>
    """

def generate_html_from_json(info_json_path, html_path):
    html_dir = create_html_directory(html_path)
    data = load_json(info_json_path)
    
    machine_info = load_json(os.path.join('temp', 'machine_info.json'))
    drives_info = machine_info.get('drives', [])
    storage_info_html = get_drive_info(drives_info)
    
    plugins = data.get('AgentInfo', {}).get('plugins', [])
    protection_info_html = get_protection_info(plugins)
    plugin_versions = get_plugin_versions(plugins)
    
    connection_data = load_json(os.path.join("temp", "json", "TestConnections.json"))
    connection_results_html = get_connection_results(connection_data)
    
    html_content = generate_html_content(data, storage_info_html, protection_info_html, plugin_versions, connection_results_html)
    
    filename = f"{data.get('AgentInfo', {}).get('host_name', 'Analyzer_Results')}_Analyzer_Results.html"
    html_path_with_name = os.path.join(html_dir, filename)

    try:
        with open(html_path_with_name, 'w', encoding='utf-8') as file:
            file.write(html_content)
    except Exception as e:
        print(f"Error writing '{html_path_with_name}': {e}")

if __name__ == "__main__":
    generate_html_from_json(os.path.join("temp", "json", "Info.json"), os.path.join("results", "{host_name}_Analyzer_Results.html"))
