from datetime import datetime, timezone
import getpass
import logging
import platform
import asyncio
import subprocess
from utils.httprequest import ServiceHttpRequests
from utils.config_reader import server_url

def get_cmd_output(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {cmd}\nError details: {e}")
        return "N/A"

async def get_system_info():
    try:
        # Json UserMetaData Details :
        info_item = {
            'userName': getpass.getuser(),
            'domainName': platform.node(),
            'osVersion': platform.version(),
            'osType': platform.machine(),
            'machineName': get_cmd_output("hostname"),
            'machineType': platform.machine(),
            'recordDateTime': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        }
        
    

        # Send MetaData Details to Server
        service_http_requests = ServiceHttpRequests(server_url)
        await service_http_requests.get_system_info(info_item)
        return info_item

    except Exception as e:
        print(f"An error occurred while getting system info: {e}")
        logging.info(f"An error occurred while getting system info: {e}")
        return None

async def main():
    system_info = await get_system_info()
    if system_info:
        print("System Information:", system_info)
    else:
        print("Failed to retrieve System Information.")

if __name__ == "__main__":
    asyncio.run(main())
