
import datetime
from email import utils
import gzip
import json
import os
import sys
import requests
from requests.exceptions import RequestException
import logging
from utils.SqlLite import SQLiteUserActivitiesDB

current_directory = os.getcwd()

# Get the parent directory
parent_directory = os.path.dirname(os.path.dirname(current_directory))



# Create a folder inside the parent directory
new_folder_path = os.path.join(parent_directory ,'AppData')
os.makedirs(new_folder_path, exist_ok=True)




# Create a file inside the new folder
file_path = os.path.join(new_folder_path, 'user_activities.db')



db = SQLiteUserActivitiesDB(file_path)

class ServiceHttpRequests:

    _jwt_token = None # Static variable for JWT token
    screenshot_value = None 

    def __init__(self, url):
        self._url = url
      

    @classmethod
    def set_jwt_token(cls, token):
        cls._jwt_token = token

    @classmethod
    def get_jwt_token(cls):
        return cls._jwt_token

    @classmethod
    def get_screenshot_value(cls):
        return cls.screenshot_value

    @classmethod
    def set_screenshot_value(cls, value):
        cls.screenshot_value = value


    
    
        
        
    async def token_authentication(self, info_data):
        logging.info("token - Inside MetaData")
        try:
            headers = {
                "Authorization": f"Bearer {self.get_jwt_token()}",
                "Content-Type": "application/json"
            }
            json_data = json.dumps(info_data)
            logging.info("token - Request Payload: %s", json_data)

            response = requests.post(f"{self._url}api/v1/monitoruser/agenttoken", headers=headers,verify = False, data=json_data)
            
            if response and response.status_code == 200:
                response_data = response.json()
                self.set_jwt_token(response_data.get('accesstoken'))
                logging.info("Token sent successfully and token updated")

                logging.info("token sent successfully and token updated")
            else:
                logging.error("Unable to send token. Status Code: %s, Response: %s", response.status_code, response.reason)
        except requests.exceptions.RequestException as ex:
            logging.error("Exception while sending token: %s", ex)
    

    async def screenshot_configuration(self, info_data):
        logging.info("screenshot config - Inside UserData")
        try:
            headers = {
                "Authorization": f"Bearer {self.get_jwt_token()}",
                "Content-Type": "application/json"
            }
            json_data = json.dumps(info_data)
            logging.info("screenshot config- Request Payload: %s", json_data)

            response = requests.post(f"{self._url}api/v1/monitoruser/screenshotconfig", headers=headers,verify = False, data=json_data)
            
            if response and response.status_code == 200:
                response_data = response.json()
                screenshot_value = response_data['result'].get('screenshot', False)
               

                self.set_screenshot_value(screenshot_value)
                logging.info("Screenshot value: %s", screenshot_value)
                

                logging.info("screenshot configuration retrieved successfully")

            else:
                screenshot_value = True
                self.set_screenshot_value(screenshot_value)
                logging.error("Unable to send  Status Code: %s, Response: %s", response.status_code, response.reason)
        except requests.exceptions.RequestException as ex:
            logging.error("Exception while sending screennshot value %s", ex)
    
  
       
    async def download_and_save_file(self,version):
                 
        try:
                machine = 'Linux'
                headers = {'Authorization': f'Bearer {self.get_jwt_token()}'}
                request_url = f"{self._url}api/monitoruser/currentversion/{version}/{machine}"
                logging.info(f"Requesting latest version from URL: {request_url}")

                response = requests.get(request_url, headers=headers,verify=False, stream=True)
                response.raise_for_status()  # Everify = Falsensure the request was successful

                # Check if the content type is 'application/zip'
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/zip':
                    # Ensure the target directory exists
                
                    latest_wheel_folder = os.path.join(parent_directory, "Latest_Wheel")
                    os.makedirs(latest_wheel_folder, exist_ok=True)
            
                    latest_dist = os.path.join(latest_wheel_folder,"MonitorUser-0.1-py3-none-any.whl")
           

                # Save the response content to the file
                with open(latest_dist, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)

                print(f"File saved successfully at: {latest_dist}")
                logging.info("file saved successfully at : {latest_dist}")               
                 
                # stop the process
                sys.exit()
                
                 
                 
                


        except requests.exceptions.RequestException as ex:
                    logging.error(f"Exception while saving file: {ex}")
                    logging.debug(f"Request URL: {request_url}")
                    logging.debug(f"Response Content: {response.content}")
                    print(f"Error in file saving: {ex}")
        except Exception as ex:
                    logging.error(f"Unexpected error: {ex}")
                    logging.debug(f"Error Details: {ex}")
                    print(f"Unexpected error: {ex}")


        
                    
        



    async def get_open_windows(self, user_data):
        logging.info("Senduseractivitiesinfo - Inside MetaData")
        try:
            logging.info(f"token for active :{self.get_jwt_token()} ")
            headers = {"Authorization": f'Bearer {self.get_jwt_token()}',"Content-Type": "application/json"}
            json_data = json.dumps(user_data)
            logging.info("Senduseractivitiesinfo - Request Payload: %s", json_data)
            response = requests.post(f"{self._url}api/monitoruser/useractivities", headers=headers,verify = False, data=json_data)
            if response and response.status_code == 200:
                logging.info("Senduseractivitiesinfo sent successfully")
                db.sync_data_to_server(self._url,self.get_jwt_token())

            else:
                db.insert_user_activity(datetime.datetime.now().isoformat(), json_data)
                logging.error("Unable to send Senduseractivities. Status Code: %s, Response: %s", response.status_code, response.text)
                
        except RequestException as ex:
            db.insert_user_activity(datetime.datetime.now().isoformat(), json_data)
            logging.error("Exception while sending Senduseractivities: %s", ex)
           

   
    

 
       
   


    async def get_system_info(self, meta_data):
        logging.info("SendSysinfo - Inside MetaData")
        logging.info(f"token for usermetadata :{self.get_jwt_token()} ")
        try:
            headers = {"Authorization": f'Bearer {self.get_jwt_token()}',"Content-Type": "application/json"}
            json_data = json.dumps(meta_data)
            logging.info("SendSysinfo - Request Payload: %s", json_data)
            response = requests.post(f"{self._url}api/monitoruser/usermetadata", headers=headers,verify=False, data=json_data)
            

            if response and response.status_code == 200:
                logging.info("SendSysinfo sent successfully")
            else:
                logging.error("Unable to send SendSysinfo. Status Code: %s, Response: %s", response.status_code, response.text)
        except requests.exceptions.RequestException as ex:
                logging.error("Exception while sending SendSysinfo: %s", ex)


        


    async def get_ipaddress_info(self, ip_data):
        logging.info("SendIpinfo - Inside MetaData")
        try:
            logging.info(f"token for ip address:{self.get_jwt_token()} ")
            headers = {"Authorization": f'Bearer {self.get_jwt_token()}',"Content-Type": "application/json"}
            # Compress the JSON data using gzip
            json_data = json.dumps(ip_data)
            compressed_data = gzip.compress(json_data.encode("utf-8"))

            logging.info("SendIpinfo - Request Payload: %s", json_data)

            # Use the compressed data in the request
            response = requests.post(
                f"{self._url}api/monitoruser/ipaddressinfo",
                headers=headers,
                verify= False,
                data=json_data
            )

            if response and response.status_code == 200:
                logging.info("SendIpinfo sent successfully")
            else:
                logging.error(
                    "Unable to send SendIpinfo. Status Code: %s, Response: %s",
                    response.status_code, response.text
                )
        except RequestException as ex:
            logging.error("Exception while sending SendIpinfo: %s", ex)

    



    async def get_senduserlogging_info(self, userlog_data):
        logging.info("senduserlogging - Inside MetaData")
        try:
            logging.info(f"token for user logging :{self.get_jwt_token()} ")
            headers = {"Authorization": f"Bearer {self.get_jwt_token()}", "Content-Type": "application/json"}
            json_data = json.dumps(userlog_data)
           
            logging.info("senduserlogging - Request Payload: %s", json_data)
            response = requests.post(f"{self._url}api/monitoruser/userlogging", headers=headers,verify = False, data=json_data)
           
            if response and response.status_code == 200:
                logging.info("senduserlogging sent successfully")
            else:
                logging.error("Unable to send senduserlogging. Status Code: %s, Response: %s", response.status_code, response.text)
        except RequestException as ex:
            logging.error("Exception while sending senduserlogging: %s", ex)


    async def send_app_version(self, user_data):
        logging.info("App version - Inside MetaData")
        try:
            headers = {"Authorization": f"Bearer {self.get_jwt_token()}", "Content-Type": "application/json"}
            json_data = json.dumps(user_data)
            logging.info("App version - Request Payload: %s", json_data)
            response = requests.post(f"{self._url}api/monitoruser/appversion", headers=headers,verify = False, data=json_data)
            if response and response.status_code == 200:
                logging.info("App version sent successfully")

            else:
               
                logging.error("Unable to send app version. Status Code: %s, Response: %s", response.status_code, response.text)
                
        except RequestException as ex:
         
            logging.error("Exception while sending app version: %s", ex)
    
    
        
    

    


   
           
        
    
