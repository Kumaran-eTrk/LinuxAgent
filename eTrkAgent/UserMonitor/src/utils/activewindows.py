import asyncio
import base64
import datetime
import getpass
import logging
import os
import platform
import subprocess
import uuid
import psutil  
from utils.get_active_window_from_image import get_window_info_from_screenshot
from utils.httprequest import ServiceHttpRequests
from utils.activity import get_idle_time
from utils.screenshot import take_screenshot
from utils.config_reader import  server_url,recorddatetime


class WindowsAccess:
    idle_ticks = 0
    total_idle_time = 0

    

async def send_app_details():
    try:

        
        
        #Get Current date and time
        # a_date = recorddatetime
    
        #Get Idle time
        idle_time_to_send = get_idle_time()
        # username=useractivityusername
        # domain=useractivitydomainname
        
        username = getpass.getuser()
        domain= platform.node()
        
        #Json data send of UserActivities and Activeapplications to server
        user_info = {
            'userName': username,
            'domainName': domain,
            'TotalIdleTime': int(idle_time_to_send),
            'CurrentDateTime':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            'ActiveApplications': get_applications(username, domain),
            'BrowserHistory': None
        }
        
        #useractivities Http Request
        
        service_http_requests = ServiceHttpRequests(server_url)
        await service_http_requests.get_open_windows(user_info)
        return user_info

    except Exception as e:
        print(f"Error in send_app_details: {e}")
        logging.info(f"Error in get_applications: {e}")
        # Log the error or handle it as needed

        # Define a function to get module name from process name
def get_module_name(pid):
    try:
        process = psutil.Process(pid)
        return process.name()
    except psutil.NoSuchProcess:
        return None

#Get the ActiveApplications
def get_applications(user_name, domain_name):
    windows = []
    try:

        

        #windows ids to find application startDateTime
        window_ids_output = subprocess.check_output(["xdotool", "search", "--onlyvisible", "--class", ""]).decode()
        window_ids = window_ids_output.splitlines()
        

        #Method used for taking the screenshot
        current_path = os.path.abspath(__file__)
        
        
       # Construct the full path to the screenshot file
        screenshot_path = os.path.join(os.path.dirname(current_path), "screenshot.png")
       
        
        take_screenshot(screenshot_path)
        
        #Used to get the active windows and application start date
        for window_id in window_ids:

            # Get the PID of the window
            pid_process = subprocess.run(["xdotool", "getwindowpid", window_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if pid_process.returncode == 0:
                pid = pid_process.stdout.strip()

                # Use psutil to get process information, including start time
                try:
                    process = psutil.Process(int(pid))
                    start_time = process.create_time()
                except psutil.NoSuchProcess:
                    continue
                
                #Get the active window title
                title_process = subprocess.run(["xdotool", "getwindowname", window_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                title = title_process.stdout.strip()
                if not title:
                    continue

                module_name = get_module_name(int(pid))
                if not module_name:
                       continue
                
               

                
               
                
                extracted_title, screenshot_data = get_window_info_from_screenshot(screenshot_path)
               
                # if the active window title matches with current active window:
                if extracted_title.lower() in title.lower() or title.lower() in extracted_title.lower():

               
                        info_item = {
                            'id': str(uuid.uuid4()),
                            'application': title,
                            'applicationname' : module_name.lower(),
                            'startDateTime': datetime.datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                            'endDateTime': recorddatetime, 
                            'screenshot': base64.b64encode(screenshot_data).decode('utf-8'),
                            'userActivityUserName': user_name,
                            'userActivityDomainName': domain_name,
                            'recordDateTime': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                        }

                  

                        windows.append(info_item)

                else:
                    local_info = {
                        'Id': str(uuid.uuid4()),
                        'Application': title,
                        'applicationname' : module_name.lower(),
                        'StartDateTime': datetime.datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                        'EndDateTime': recorddatetime,
                        'Screenshot': None,
                        'UserActivityUserName': user_name,
                        'UserActivityDomainName': domain_name,
                        'RecordDateTime': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                    }
                    windows.append(local_info)
            else:
                continue

    except Exception as e:
        print(f"Error in get_applications: {e}")
        logging.info(f"Error in get_applications: {e}")
        raise  

    return windows

async def main():
    await send_app_details()



if __name__ == "__main__":
    # Setup logging configuration
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    # Run the main coroutine using asyncio.run() for simplicity
    asyncio.run(main())
