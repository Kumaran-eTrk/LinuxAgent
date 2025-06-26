import asyncio
import logging
from utils.httprequest import ServiceHttpRequests
from utils.config_reader import server_url,productkey



async def send_token():
        
        try:
            # Json UserMetaData Details :
            info_item = {
                'productkey' : productkey,
                'role': 'Agent',
                
            }

            # Send MetaData Details to Server
            
            service_http_requests = ServiceHttpRequests(server_url)
            await service_http_requests.token_authentication(info_item)
            return info_item

        except Exception as e:
            print(f"An error occurred while getting send token info: {e}")
            logging.info(f"An error occurred while getting send token info: {e}")
            return None
        
async def main():
    system_info = await send_token
    if system_info:
        print("send token Information:", system_info)
    else:
        print("Failed to retrieve send token.")
if __name__ == "__main__":
    asyncio.run(main())
