import json
import logging
import sqlite3
import utils
import requests

import utils.sendtoken


class SQLiteUserActivitiesDB:
    def __init__(self,db_file):
    
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    

    def create_table(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_activities (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_data TEXT, 
                                    timestamp TEXT
                                    )''')
            self.conn.commit()
        except Exception as e: 
            logging.error("Error occurred during database creation: %s", e)  


    def insert_user_activity(self, timestamp, user_data):
        try:
            utils.sendtoken.send_token()
            logging.info("Backup is running")
            self.cursor.execute('''INSERT INTO user_activities (user_data,timestamp)
                                    VALUES (?, ?)''', (user_data,timestamp))
            self.conn.commit()
            logging.info("Data inserted successfully in local storage")
        except Exception as e:
            logging.error("Error occurred during database insertion: %s", e)

    def close_connection(self):
        if self.conn:
            self.conn.close()

    def retrieve_data_to_sync(self):
        try:
            logging.info("Retreiving the Data...")
            self.cursor.execute("SELECT * FROM user_activities")
            unsynced_data = self.cursor.fetchall()
            logging.info("Data Retreived...")
            return unsynced_data
        
        except Exception as e:
            logging.error("Error occurred during data retrieval: %s", e)

    def delete_synced_data(self):
        try:
            self.cursor.execute("DELETE  FROM user_activities")
            self.conn.commit()
            logging.info("Data deleted from local storage.... ")
        except Exception as e:
            logging.error("Error occurred during data deletion: %s", e)
    
    def refresh_synced_data(self):
        try:
            logging.info("Cleaning the Data...")
            self.cursor.execute("VACUUM")
            logging.info("Data Cleaned from the local storage.... ")
        except Exception as e:
            logging.error("Error occurred during data deletion: %s", e)


    def sync_data_to_server(self,url,token):
        logging.info("Syncing data to server...")
        try:
            # Retrieve data from SQLite database
            data_to_sync = self.retrieve_data_to_sync()

            if data_to_sync:
               
                
                for data_item in data_to_sync:
                    # Convert each data item to JSON
                    user_data = data_item[1] 
                    user_id = data_item[0]
                    # Send data to server
                    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
                    response = requests.post(f"{url}api/monitoruser/useractivities", headers=headers, verify = False,data=user_data)
                    if response and response.status_code == 200:
                        # Data synced successfully, delete from local database
                        self.delete_synced_data()
                        logging.info("Data synced to server successfully")
                    else:
                        logging.error("Failed to sync data to server. Status Code: %s, Response: %s", response.status_code, response.reason)



                self.refresh_synced_data();  

            else:
                logging.info("No data to sync from local storage")
        except Exception as ex:
                logging.error("Exception occurred during data syncing: %s", ex)