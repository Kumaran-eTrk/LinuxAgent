import asyncio
import datetime
import getpass
import logging
import socket
import netifaces
from getmac import get_mac_address as get_mac
from utils.httprequest import ServiceHttpRequests
from utils.config_reader import  server_url,  recorddatetime

class IPAddressInfo:
    def __init__(self, username, ip_address, mac_address, record_datetime):
        self.UserName = username
        self.IPAddress = ip_address
        self.MacAddress = mac_address
        self.RecordDateTime = record_datetime

def get_local_ip_and_mac(remote_ip):
    local_ip = ''
    mac_address = ''
    remote_port = 443

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_client:
            udp_client.connect((remote_ip, remote_port))
            local_ip = udp_client.getsockname()[0]

            # Get MAC address using netifaces library
            mac_address = get_mac_address(local_ip)

            # Fallback to get_mac library if netifaces fails
            if mac_address is None:
                mac_address = get_mac(ip=local_ip)
    except Exception as e:
        print(f"An error occurred while getting local IP and MAC: {e}")
        logging.info(f"An error occurred while getting local IP and MAC: {e}")
    return local_ip, mac_address

def get_mac_address(ip_address):
    try:
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            if netifaces.AF_LINK in netifaces.ifaddresses(interface):
                if netifaces.AF_INET in netifaces.ifaddresses(interface):
                    if netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr'] == ip_address:
                        return netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
    except Exception as e:
        print(f"Error getting MAC address using netifaces: {e}")
        logging.info(f"Error getting MAC address using netifaces: {e}")
    return None

async def get_ipaddress_info():
    try:
        remote_ip_address = ""  
        local_ip_address, mac_address = get_local_ip_and_mac(remote_ip_address)
        a_date = recorddatetime
        info_item = {
            'userName': getpass.getuser(),
            'iPAddress': local_ip_address,
            'recordDateTime': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            'macAddress': mac_address,
        }
        
        service_http_requests = ServiceHttpRequests(server_url)
        await service_http_requests.get_ipaddress_info(info_item)
        return info_item
    except Exception as e:
        print(f"An error occurred while getting IP address info: {e}")
        logging.info(f"An error occurred while getting IP address info: {e}")
        return None

async def main():
    system_info = await get_ipaddress_info()
    if system_info:
        print("IP Information:", system_info)
    else:
        print("Failed to retrieve IP Information.")

if __name__ == "__main__":
    asyncio.run(main())
