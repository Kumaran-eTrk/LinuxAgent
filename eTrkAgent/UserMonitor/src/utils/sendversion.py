import asyncio
import getpass
import logging
import os
import platform
from utils.httprequest import ServiceHttpRequests
from utils.config_reader import server_url



async def send_version(version):
        

        try:
            # Json UserMetaData Details :
            info_item = {
                'userName': getpass.getuser(),
                'domainName': platform.node(),
                'version': version,
               
            }

            # Send MetaData Details to Server
            
            service_http_requests = ServiceHttpRequests(server_url)
            await service_http_requests.send_app_version(info_item)
            # await service_http_requests.download_and_save_file(version)
            return info_item

        except Exception as e:
            print(f"An error occurred while getting send app version info: {e}")
            logging.info(f"An error occurred while getting send app version info: {e}")
            return None
        
async def main():
    system_info = await send_version()
    if system_info:
        print("App Version Information:", system_info)
    else:
        print("Failed to retrieve App Version.")
if __name__ == "__main__":
    asyncio.run(main())
