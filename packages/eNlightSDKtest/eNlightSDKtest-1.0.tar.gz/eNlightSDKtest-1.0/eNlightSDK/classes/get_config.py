import json
config_path = ""

def get_config_data():
    try:
        with open(config_path + "config", "r") as config_file:
            config_data = config_file.read().strip()  # Read the file content
            
            if config_data:  # Ensure there's content in the file
                config_json = json.loads(config_data)  # Attempt to parse JSON
                
                # If the JSON parsing is successful, return the config data
                return config_json
            else:
                print("Config file is empty.")
                return {}  # Return an empty dictionary if file is empty
            
    except FileNotFoundError:
        print("Config file not found.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {}
