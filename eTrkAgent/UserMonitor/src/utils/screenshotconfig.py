import asyncio
import getpass
import logging
import platform
from utils.httprequest import ServiceHttpRequests
from utils.config_reader import server_url


async def screenshot_configuration():
        
        try:
            # Json UserMetaData Details :
            info_item = {
               'Username': getpass.getuser(),
               'Domainname': platform.node(),  
            }

            # Send MetaData Details to Server
            
            service_http_requests = ServiceHttpRequests(server_url)
            await service_http_requests.screenshot_configuration(info_item)
            return info_item

        except Exception as e:
            print(f"An error occurred while getting send screenshot config: {e}")
            logging.info(f"An error occurred while getting send screenshot config: {e}")
            return None
        
async def main():
    system_info = await screenshot_configuration()
    if system_info:
        print("screenshot Information:", system_info)
    else:
        print("Failed to retrieve send screenshot config.")
if __name__ == "__main__":
    asyncio.run(main())
