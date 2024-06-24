# testconnection_to_json.py

import json
import re

def convert_test_connection_to_json(test_connection_path, test_connection_output):
    try:
        with open(test_connection_path, 'r') as connection_file:
            connection_data = connection_file.read()
        

        pattern = re.compile(r'\{[^\}]*?\}', re.DOTALL)
        blocks = pattern.findall(connection_data)
        
        test_values = []
        for block in blocks:
            try:
                data = json.loads(block)
                if "UriTested" in data:
                    formatted_output = {
                        "UriTested": data["UriTested"],
                        "Message": data["Message"],
                        "StatusCode": data["StatusCode"],
                        "ExpectedStatusCode": data["ExpectedStatusCode"],
                        "Result": data["Result"],
                        "Headers": data["Headers"]
                    }
                    test_values.append(formatted_output)  # Collect all valid blocks
            except json.JSONDecodeError as e:
                print(f"Error reading file {test_connection_path}: {e}")

        with open(test_connection_output, 'w') as outfile:
            json.dump(test_values, outfile, indent=4)
        
        return test_values  # Return the list of formatted outputs
    except Exception as e:
        print(f"An error occurred: {e}")
        return None