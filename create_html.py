import json
import os

def bytes_to_gb(bytes_value):
    gb_value = bytes_value / (1024 ** 3)
    return gb_value

def generate_html_from_json(info_json_path, html_path):
    html_dir = os.path.dirname(html_path)
    if html_dir:
        os.makedirs(html_dir, exist_ok=True)
    
    try:
        with open(info_json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{info_json_path}' not found.")
        return
    except Exception as e:
        print(f"Error reading '{info_json_path}': {e}")
        return
    
    agent_info = data.get('AgentInfo', {})
    account_token = data.get('AccountToken', 'N/A')
    nebula_machine_id = data.get('NebulaMachineId', 'N/A')
    host_name = agent_info.get('host_name', 'N/A')
    fully_qualified_host_name = agent_info.get('fully_qualified_host_name', 'N/A')
    last_user = agent_info.get('last_user', 'N/A')
    engine_version = agent_info.get('engine_version', 'N/A')

    os_version = agent_info.get('os_info', {}).get('os_version', 'N/A')
    os_release_name = agent_info.get('os_info', {}).get('os_release_name', 'N/A')
    os_type = agent_info.get('os_info', {}).get('os_type', 'N/A')
    os_architecture = agent_info.get('os_info', {}).get('os_architecture', 'N/A')

    try:
        with open(os.path.join('logs', 'PluginsData', 'AssetManager', 'machine_info.json'), 'r', encoding='utf-8') as machine_file:
            machine_info = json.load(machine_file)
    except FileNotFoundError:
        print("Error: File 'machine_info.json' not found.")
        machine_info = {}

    drives_info = machine_info.get('drives', [])

    storage_info_html = ''
    for drive in drives_info:
        drive_name = drive.get('name', 'N/A')
        volume_label = drive.get('volume_label', 'N/A')
        drive_format = drive.get('drive_format', 'N/A')
        total_size_bytes = drive.get('total_size', 0)
        freespace_available_bytes = drive.get('freespace_available', 0)
        freespace_total_bytes = drive.get('freespace_total', 0)

        total_size_gb = bytes_to_gb(total_size_bytes)
        freespace_available_gb = bytes_to_gb(freespace_available_bytes)
        freespace_total_gb = bytes_to_gb(freespace_total_bytes)

        storage_used_gb = total_size_gb - freespace_available_gb
        if total_size_gb > 0:
            storage_used_percentage = (storage_used_gb / total_size_gb) * 100
        else:
            storage_used_percentage = 0

        storage_percentage_display = f"{storage_used_percentage:.2f}%"

        storage_info_html += f"""
        <div class="info-item">
            <label>Drive name:</label>
            <span>{drive_name}</span>
        </div>
        <div class="info-item">
            <label>Volume label:</label>
            <span>{volume_label}</span>
        </div>
        <div class="info-item">
            <label>Drive format:</label>
            <span>{drive_format}</span>
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

    plugins = agent_info.get('plugins', [])
    protection_status = next((p.get('protection_status', {}) for p in plugins if p.get('product_name') == 'Endpoint Protection'), {})
    rtp = protection_status.get('rtp', 'N/A')
    ae = protection_status.get('ae', 'N/A')
    arw = protection_status.get('arw', 'N/A')
    mwac = protection_status.get('mwac', 'N/A')
    sp = protection_status.get('sp', 'N/A')

    endpoint_protection = next((p.get('plugin_version', 'N/A') for p in plugins if p.get('product_name') == 'Endpoint Protection'), 'N/A')
    protection_update = next((p.get('update_package_version', 'N/A') for p in plugins if p.get('product_name') == 'Endpoint Protection'), 'N/A')
    protection_service = next((p.get('sdk_version', 'N/A') for p in plugins if p.get('product_name') == 'Endpoint Protection'), 'N/A')
    component_package = next((p.get('component_package_version', 'N/A') for p in plugins if p.get('product_name') == 'Endpoint Protection'), 'N/A')
    active_response_shell = next((p.get('plugin_version', 'N/A') for p in plugins if p.get('product_name') == 'Active Response Shell'), 'N/A')
    brute_force_protection = next((p.get('plugin_version', 'N/A') for p in plugins if p.get('product_name') == 'Windows Remote Intrusion Detection and Prevention'), 'N/A')
    asset_manager = next((p.get('plugin_version', 'N/A') for p in plugins if p.get('product_name') == 'Asset Manager'), 'N/A')
    edr = next((p.get('plugin_version', 'N/A') for p in plugins if p.get('product_name') == 'Endpoint Detection and Response'), 'N/A')

    rtp_display = rtp.capitalize()
    ae_display = ae.capitalize()
    arw_display = arw.capitalize()
    mwac_display = mwac.capitalize()
    sp_display = sp.capitalize()

    def get_indicator_symbol(status):
        return '✔' if status == 'started' else '✖'

    rtp_indicator_symbol = get_indicator_symbol(rtp)
    ae_indicator_symbol = get_indicator_symbol(ae)
    arw_indicator_symbol = get_indicator_symbol(arw)
    mwac_indicator_symbol = get_indicator_symbol(mwac)
    sp_indicator_symbol = get_indicator_symbol(sp)

    def connection_indicator_symbol(status):
        return '✔' if status == 'Passed' else '✖'

    try:
        with open(os.path.join('logs', 'Analyzer', 'TestConnections.json'), 'r', encoding='utf-8') as connection_file:
            connection_data = json.load(connection_file)
    except FileNotFoundError:
        print("Error: File 'TestConnections.json' not found.")
        connection_data = {}

    connection_results_html = ''
    for url, details in connection_data.items():
        status = "Passed" if details.get('Result', False) else "Failed"
        symbol = connection_indicator_symbol(status)
        connection_results_html += f'<div class="info-item-connection"><label>{url}</label><span class="indicator">{symbol}</span><span>{status}</span></div>\n'

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{host_name} Results</title>
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
                width: 325px; /* Increased width */
                font-weight: bold;
            }}
            .info-item-connection label {{
                display: inline-block;
                width: 670px; /* Increased width */
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
                color: #808080; /* Light grey background */
                padding: 10px;
                margin-top: 20px;
            }}
            .grey-background a {{
                color: #808080; /* Darker text color for links */
                text-decoration: none; /* Remove underline */
                font-weight: bold; /* Make the link text bold */
            }}
            .grey-background a:hover {{
                text-decoration: underline; /* Underline on hover */
            }}
            .storage-bar-container {{
                width: 90%;
                height: 10px; /* Adjust height as needed */
                background-color: #f0f0f0; /* Background color of the bar */
                border-radius: 5px; /* Rounded corners */
                margin-top: 5px;
                overflow: hidden; /* Ensure the bar doesn't overflow its container */
            }}

            .storage-bar {{
                height: 100%;
                background-color: #4caf50; /* Color of the progress */
            }}
        </style>
    </head>
    <body>
        
        <h1>Endpoint Agent Analyzer Results</h1>

        <div class="info-item">
            <label>Account Token:</label>
            <span>{account_token}</span>
        </div>
        <div class="info-item">
            <label>Nebula Machine ID:</label>
            <span>{nebula_machine_id}</span>
        </div>
        <hr>
        
        <div class="left-column">
            <h3>General Information</h3>
            <div class="info-item">
                <label>Endpoint Name:</label>
                <span>{host_name}</span>
            </div>
            <div class="info-item">
                <label>FQDN:</label>
                <span>{fully_qualified_host_name}</span>
            </div>
            <div class="info-item">
                <label>Last User:</label>
                <span>{last_user}</span>
            </div>

            <h3>Operating System</h3>
            <div class="info-item">
                <label>OS Version:</label>
                <span>{os_version}</span>
            </div>
            <div class="info-item">
                <label>OS Friendly Name:</label>
                <span>{os_release_name}</span>
            </div>
            <div class="info-item">
                <label>OS Type:</label>
                <span>{os_type}</span>
            </div>
            <div class="info-item">
                <label>OS Architecture:</label>
                <span>{os_architecture}</span>
            </div>
            
            <div class="info-item">
                <h3>Storage Information:</h3>
            </div>
            {storage_info_html}
        </div>

        <div class="right-column">
            <h3>Protection Status</h3>
            <div class="info-item">
                <label>Web Protection:</label>
                <span class="indicator">{mwac_indicator_symbol}</span><span>{mwac_display}</span>
            </div>
            <div class="info-item">
                <label>Malware Protection:</label>
                <span class="indicator">{rtp_indicator_symbol}</span><span>{rtp_display}</span>
            </div>
            <div class="info-item">
                <label>Exploit Protection:</label>
                <span class="indicator">{ae_indicator_symbol}</span><span>{ae_display}</span>
            </div>
            <div class="info-item">
                <label>Behavior Protection:</label>
                <span class="indicator">{arw_indicator_symbol}</span><span>{arw_display}</span>
            </div>
            <div class="info-item">
                <label>Self Protection:</label>
                <span class="indicator">{sp_indicator_symbol}</span><span>{sp_display}</span>
            </div>

            <h3>Agent and Plugins</h3>
            <div class="info-item">
                <label>Endpoint Agent:</label>
                <span>{engine_version}</span>
            </div>
            <div class="info-item">
                <label>Endpoint Protection:</label>
                <span>{endpoint_protection}</span>
            </div>
            <div class="info-item">
                <label>Protection Update:</label>
                <span>{protection_update}</span>
            </div>
            <div class="info-item">
                <label>Protection Service:</label>
                <span>{protection_service}</span>
            </div>
            <div class="info-item">
                <label>Component Package:</label>
                <span>{component_package}</span>
            </div>
            <br>
            <div class="info-item">
                <label>Active Response Shell:</label>
                <span>{active_response_shell}</span>
            </div>
            <br>
            <div class="info-item">
                <label>Brute Force Protection:</label>
                <span>{brute_force_protection}</span>
            </div>
            <br>
            <div class="info-item">
                <label>Asset Manager:</label>
                <span>{asset_manager}</span>
            </div>
            <br>
            <div class="info-item">
                <label>Endpoint Detection and Response:</label>
                <span>{edr}</span>
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
    
    filename = f"{host_name}_Analyzer_Results.html"
    html_path_with_name = os.path.join(html_dir, filename)

    try:
        with open(html_path_with_name, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"HTML file '{filename}' generated successfully.")
    except Exception as e:
        print(f"Error writing '{html_path_with_name}': {e}")

if __name__ == "__main__":
    generate_html_from_json(os.path.join('logs', 'Analyzer', 'Info.json'), os.path.join('logs', 'Analyzer', '{host_name}_Analyzer_Results.html'))