import configparser
import datetime
import os

# Global variable to store configuration
config_data = {}


def load_config(file_path):
    global config_data
   
   
    # print("Attempting to load configuration from:", file_path)

    # Convert to absolute path
    file_path = os.path.abspath(file_path)
    
    parser = configparser.ConfigParser()
    try:
        with open(file_path, 'r') as config_file:
            parser.read_file(config_file)

        for section in parser.sections():
            config_data[section] = dict(parser.items(section))
          
            

        print("Configuration loaded successfully.")
        # print("Config Data:", config_data)

    except FileNotFoundError:
        print(f"Error: Configuration file not found at {file_path}")

# Load the configuration when the module is imported
load_config('config.ini')


# Define db_host and server_port after loading the configuration
log_path=config_data.get('path',{}).get('log_path','')
version = config_data.get('version',{}).get('version','')
productkey = config_data.get('productkey',{}).get('key','')
service = config_data.get('service',{}).get('processname','')
server_url = config_data.get('server', {}).get('server_url', '')
screenshot_path=config_data.get('path',{}).get('screenshot_path','')

recorddatetime=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

interval_1 = int(config_data.get('timeintervals', {}).get('interval_1', 0))
interval_2 = int(config_data.get('timeintervals', {}).get('interval_2', 0))
interval_3 = int(config_data.get('timeintervals', {}).get('interval_3', 0))
interval_4 = int(config_data.get('timeintervals', {}).get('interval_4', 0))
interval_5 = int(config_data.get('timeintervals', {}).get('interval_5', 0))










