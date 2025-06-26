import datetime
import asyncio
import getpass
import platform
import subprocess
from utils.httprequest import ServiceHttpRequests
from utils.config_reader import  server_url,recorddatetime






def get_cmd_output(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {cmd}\nError details: {e}")
        return "N/A"

async def get_userlogging_info():
    try:
        a_date = recorddatetime
        who_output = get_cmd_output("who")
        date_str, time_str = who_output.split()[2:4]
        date_time_str = f"{date_str} {time_str}"
        local_datetime = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
        utc_offset = datetime.datetime.now(datetime.timezone.utc).astimezone().utcoffset()
        utc_datetime = local_datetime - utc_offset

        # Json Data of UserLoggingActivity
        info_item = {
            'userName': getpass.getuser(),
            'domainName': platform.node(),
            'currentDateTime':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            'lastLogonDateTime': utc_datetime.strftime('%Y-%m-%dT%H:%M:%S.485Z')
        }

        # Send UserLoggingActivity Data to Server
   
        service_http_requests = ServiceHttpRequests(server_url)
        await service_http_requests.get_senduserlogging_info(info_item)
        return info_item

    except Exception as e:
        print(f"An error occurred while getting user logging info: {e}")
        return None



async def main():
    system_info = await get_userlogging_info()
    if system_info:
        print("UserLoggingInfo Information:", system_info)
    else:
        print("Failed to retrieve UserLoggingInfo.")

if __name__ == "__main__":
    asyncio.run(main())
