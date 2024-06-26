import json
import os

def slice_json(info_txt_path):
    try:
        # Check if the file exists
        if not os.path.isfile(info_txt_path):
            print(f"Error: File {info_txt_path} does not exist.")
            return None
        
        with open(info_txt_path, "r") as info_file:
            content = info_file.read()
        
        # Split lines
        lines = content.splitlines()

        data = {}
        json_content = ""
        in_json_section = False

        for line in lines:
            # Check for the "Agent Info" section
            if "Agent Info=" in line:
                in_json_section = True
                json_content += line.split("=", 1)[1].strip()
            elif in_json_section:
                json_content += line.strip()
            elif "=" in line:
                key, value = line.split("=", 1)
                data[key.strip()] = value.strip()
        
        # Parse the JSON section
        if json_content:
            agent_info = json.loads(json_content)
            data["AgentInfo"] = agent_info

        return data
    
    except IOError as e:
        print(f"Error reading file {info_txt_path}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON content in {info_txt_path}: {e}")
        return None
    except Exception as e:
        print(f"Error processing file {info_txt_path}: {e}")
        return None