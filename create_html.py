import json
import os

from datetime import datetime

script_version = "v.0.5.6"

def get_run_timestamp():
    # Get the current date and time
    now = datetime.now()
    
    # Format the date and time as a string in the desired format
    timestamp = now.strftime("%I:%M %p, %d/%m/%Y")
    
    return timestamp

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

def trim_version(version):
    parts = version.split('.')
    if len(parts) >= 4:
        return f"{parts[0]}.{parts[1]}.{parts[3]}"
    return version  # Return original version if format is unexpected

def get_plugin_versions(plugins):
    plugin_version_map = {
        'Endpoint Protection': 'endpoint_protection',
        'Active Response Shell': 'active_response_shell',
        'Windows Remote Intrusion Detection and Prevention': 'brute_force_protection',
        'Asset Manager': 'asset_manager',
        'Endpoint Detection and Response': 'edr',
    }

    plugin_info = {key: trim_version(next((p.get('plugin_version', 'N/A') for p in plugins if p.get('product_name') == key), 'N/A')) for key in plugin_version_map}
    return plugin_info

def get_services(state):
    services_state_map = {
        'Malwarebytes Endpoint Agent Monitor': 'ea_monitor',
        'Malwarebytes Service': 'mbam_service',
        'Malwarebytes Endpoint Agent': 'ea_service',
        'ThreatDown Endpoint Agent': 'ea_service'
    }

    service_info = {
        'ea_monitor': 'N/A',
        'mbam_service': 'N/A',
        'ea_service': 'N/A'
    }

    for s in state:
        caption = s.get('Caption', '')
        state_value = s.get('State', 'N/A')
        if caption in services_state_map:
            internal_name = services_state_map[caption]
            # Only update if the current value is 'N/A'
            if service_info[internal_name] == 'N/A':
                service_info[internal_name] = state_value

    return service_info

def get_drive_info(drives):
    storage_info_html = '''
    
    <table class="storage_info">
        <tr>
            <th>Drive Name</th>
            <th>Volume Label</th>
            <th>Drive Format</th>
            <th style="text-align: right;">Used Storage (GB)</th>
            <th style="text-align: right;">Total Storage (GB)</th>
            <th style="text-align: right;">Free Space Available (GB)</th>
            <th style="text-align: right;">Percentage Used</th>
        </tr>
        <hr>
        <h2 style="margin-bottom: -5px;">Storage Information</h2>
    '''
    for idx, drive in enumerate(drives):
        total_size_gb = bytes_to_gb(drive.get('total_size', 0))
        freespace_available_gb = bytes_to_gb(drive.get('freespace_available', 0))
        storage_used_gb = total_size_gb - freespace_available_gb
        storage_used_percentage = (storage_used_gb / total_size_gb) * 100 if total_size_gb > 0 else 0
        storage_percentage_display = f"{storage_used_percentage:.2f}%"

        storage_info_html += f"""
        <tr style="background-color: {'#d9d9d9' if idx % 2 == 0 else '#ffffff'};">
            <td>{drive.get('name', 'N/A')}</td>
            <td>{drive.get('volume_label', 'N/A')}</td>
            <td>{drive.get('drive_format', 'N/A')}</td>
            <td style="text-align: right;">{storage_used_gb:.2f}</td>
            <td style="text-align: right;">{total_size_gb:.2f}</td>
            <td style="text-align: right;">{freespace_available_gb:.2f}</td>
            <td style="text-align: right;">{storage_percentage_display}</td>
        </tr>
        """
    storage_info_html += '</table>'
    return storage_info_html

def get_connection_results(connection_data):
    connection_results_html = '''
    <table class="connection_results">
        <tr>
            <th>URL</th>
            <th>Status</th>
        </tr>
        <hr>
        <h2 style="margin-bottom: -5px;">Test Connection Results</h2>
    '''
    def connection_indicator_symbol(status):
        return "✔" if status == "Passed" else "✖"

    for idx, (url, details) in enumerate(connection_data.items()):
        status = "Passed" if details.get("Result", False) else "Failed"
        symbol = connection_indicator_symbol(status)
        status_class = "status-passed" if status == "Passed" else "status-failed"
        connection_results_html += f'''
        <tr style="background-color: {'#d9d9d9' if idx % 2 == 0 else '#ffffff'};">
            <td>{url}</td>
            <td class="{status_class}">{symbol} {status}</td>
        </tr>
        '''
    connection_results_html += '</table>'
    return connection_results_html

def format_system_uptime(uptime):
    parts = uptime.split('.')
    days = parts[0]
    time_str = parts[1]
    hours, minutes, seconds = time_str.split(':')
    return f"{days}d {hours}h {minutes}min {int(float(seconds))}s"

def format_status(status):
    if status.lower() in ['started', 'running']:
        return f'<span style="color: green;">✔ {status.title()}</span>'
    elif status.lower() == 'n/a':
        return f'<span style="color: black;">— {status.title()}</span>'
    else:
        return f'<span style="color: red;">✖ {status.title()}</span>'

def format_services(service_info):
    formatted_services = {}
    for service, status in service_info.items():
        formatted_services[service] = format_status(status)
    return formatted_services

def generate_html_content(data, storage_info_html, plugin_versions, connection_results_html, system_uptime, services_info):
    agent_info = data.get('AgentInfo', {})

    protection_statuses = {}
    for plugin in agent_info.get('plugins', []):
        if plugin.get('product_name') == 'Endpoint Protection':
            protection_statuses = plugin.get('protection_status', {})
            break

    formatted_services = format_services(services_info)

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
                width: 50%;
            }}
            .info-item-connection label {{
                display: inline-block;
                width: 670px;
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

            table {{
                border-collapse: collapse;
                width: 100%;
                table-layout:fixed;
            }}

            td, th {{
                border: 0px solid #dddddd;
                text-align: left;
                padding: 8px;
                font-weight: normal;
            }}

            .data_table tr:nth-child(even), .storage_info tr:nth-child(even), .connection_results tr:nth-child(even) {{
                background-color: #d9d9d9;
            }}

            td:nth-child(1), td:nth-child(3), th:nth-child(1), th:nth-child(3) {{
                font-weight: bold;
            }}

            td.table_category, th.table_category {{
                font-weight: bold;
                font-size: 150%;
            }}

            /* Specific styles for storage information and test connection tables */
            .storage_info th, .connection_results th {{
                font-weight: bold;
            }}

            .storage_info td, .connection_results td {{
                font-weight: normal;
            }}

            .connection_results .status-passed {{
                color: green;
            }}

            .connection_results .status-failed {{
                color: red;
            }}
        </style>
    </head>
    <body>
        <h1>Endpoint Agent Analyzer Results</h1>
        <div class="info-item">
            <label><span style="font-weight: bold;">Script Version:</span> {script_version} | <span style="font-weight: bold;">Script RunTime:</span> {get_run_timestamp()}</label>
        </div>
        <br>
        
        <!-- Account Token and Nebula Machine ID Information -->
        <table>
        <tr>
        <th>Account Token:</th>
        <th colspan="3">{data.get('AccountToken', 'N/A')}</th>
        </tr>
        <tr>
        <th>Nebula Machine ID:</th>
        <th colspan="3">{data.get('NebulaMachineId', 'N/A')}</th>
        </tr>
        </table>
        <hr>

        <!-- General Information and Operating System Information -->
        <div>
        <table class="data_table">
        <tr>
        <th  colspan="2" class="table_category">General Information</th>
        <th colspan="2" class="table_category">Operating System</th>
        </tr>
        <tr>
        <th>Endpoint Name:</th>
        <th>{agent_info.get('host_name', 'N/A')}</th>
        <th>OS Version:</th>
        <th>{agent_info.get('os_info', {}).get('os_version', 'N/A')}</th>
        </tr>
        <tr>
        <th>FQDN</th>
        <th>{agent_info.get('fully_qualified_host_name', 'N/A')}</th>
        <th>OS Friendly Name:</th>
        <th>{agent_info.get('os_info', {}).get('os_release_name', 'N/A')}</th>
        </tr>
        <tr>
        <th>Last User:</th>
        <th>{agent_info.get('last_user', 'N/A')}</th>
        <th>OS Type:</th>
        <th>{agent_info.get('os_info', {}).get('os_type', 'N/A')}</th>
        </tr>
        <tr>
        <th>System Uptime</th>
        <th>{system_uptime}</th>
        <th>OS Architecture:</th>
        <th>{agent_info.get('os_info', {}).get('os_architecture', 'N/A')}</th>
        </tr>
        </table>
        <hr>
        </div>
        
        <!-- Protection Status and Agent and Plugins Information -->
        <div>
        <table class="data_table">
        <tr>
        <th  colspan="2" class="table_category">Protection Status</th>
        <th colspan="2" class="table_category">Agent and Plugins</th>
        </tr>
        <tr>
        <th>Malware Protection:</th>
        <th>{format_status(protection_statuses.get('rtp', 'N/A'))}</th>
        <th>Endpoint Agent:</th>
        <th>{trim_version(agent_info.get('engine_version', 'N/A'))}</th>
        </tr>
        <tr>
        <th>Exploit Protection:</th>
        <th>{format_status(protection_statuses.get('ae', 'N/A'))}</th>
        <th>Endpoint Protection:</th>
        <th>{plugin_versions['Endpoint Protection']}</th>
        </tr>
        <tr>
        <th>Behavior Protection:</th>
        <th>{format_status(protection_statuses.get('arw', 'N/A'))}</th>
        <th>Active Response Shell:</th>
        <th>{plugin_versions['Active Response Shell']}</th>
        </tr>
        <tr>
        <th>Web Protection:</th>
        <th>{format_status(protection_statuses.get('mwac', 'N/A'))}</th>
        <th>Brute Force Protection:</th>
        <th>{plugin_versions['Windows Remote Intrusion Detection and Prevention']}</th>
        </tr>
        <tr>
        <th>Self Protection:</th>
        <th>{format_status(protection_statuses.get('sp', 'N/A'))}</th>
        <th>Asset Manager:</th>
        <th>{plugin_versions['Asset Manager']}</th>
        </tr>
        <tr>
        <th></th>
        <th></th>
        <th>Endpoint Detection and Response:</th>
        <th>{plugin_versions['Endpoint Detection and Response']}</th>
        </tr>
        <tr>
        <th></th>
        <th></th>
        <th>User Agent:</th>
        <th>{", ".join([trim_version(v) for v in agent_info.get('tray_version', [])])}</th>
        </tr>
        <tr>
        <th></th>
        <th></th>
        <th>Service Version:</th>
        <th>{trim_version(agent_info.get('service_version', 'N/A'))}</th>
        </tr>
        </table>
        </div>

        <!-- Services and Processes Information-->
        <div>
        <table class="data_table">
        <tr>
        <th  colspan="2" class="table_category">Services</th>
        <th colspan="2" class="table_category">Processes [WIP]</th>
        </tr>
        <tr>
        <th>Malwarebytes Service:</th>
        <th>{formatted_services.get('mbam_service', 'N/A')}</th>
        <th>MBAMService.exe</th>
        <th></th>
        </tr>
        <tr>
        <th>Endpoint Agent:</th>
        <th>{formatted_services.get('ea_service', 'N/A')}</th>
        <th>MBCloudEA.exe</th>
        <th></th>
        </tr>
        <tr>
        <th>Endpoint Agent Monitor</th>
        <th>{formatted_services.get('ea_monitor', 'N/A')}</th>
        <th>EAServiceMonitor.exe</th>
        <th></th>
        </tr>
        <tr>
        <th></th>
        <th></th>
        <th>EATray.exe</th>
        <th></th>
        </tr>
        <tr>
        <th>VPN Service</th>
        <th></th>
        <th>MBVpnService.exe</th>
        <th></th>
        </tr>
        <tr>
        <th>VPN Tunnel Service</th>
        <th></th>
        <th></th>
        <th></th>
        </tr>
        
        </div>
        <hr>

        <!-- Storage Information -->
        <div class="storage_info">
            {storage_info_html}
        </div>
        <!-- Test Connection Results Information -->
        <div class="connection_results">
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
    plugin_versions = get_plugin_versions(plugins)
    
    connection_data = load_json(os.path.join("temp", "json", "TestConnections.json"))
    connection_results_html = get_connection_results(connection_data)
    
    system_info = load_json(os.path.join('temp', 'SystemInfo.json'))
    system_uptime = format_system_uptime(system_info.get('SystemUptime', '0.00:00:00'))

    services_info = get_services(load_json(os.path.join("temp", "json", "Services.json")))

    html_content = generate_html_content(data, storage_info_html, plugin_versions, connection_results_html, system_uptime, services_info)
    
    host_name = data.get('AgentInfo', {}).get('host_name', 'Analyzer_Results')
    filename = f"{host_name}_Analyzer_Results.html"
    html_path_with_name = os.path.join(html_dir, filename)

    try:
        with open(html_path_with_name, 'w', encoding='utf-8') as file:
            file.write(html_content)
    except Exception as e:
        print(f"Error writing '{html_path_with_name}': {e}")

    return host_name, html_path_with_name


if __name__ == "__main__":
    generate_html_from_json(os.path.join("temp", "json", "Info.json"), os.path.join("results", "Analyzer_Results.html"))
