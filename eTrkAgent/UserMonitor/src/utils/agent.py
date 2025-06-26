import configparser
from datetime import datetime, timedelta
import sys
import os
import time
import atexit
from signal import SIGTERM 
import asyncio
import logging
import logging.handlers
from utils.sendtoken import send_token
from utils.sysinfo import get_system_info
from utils.activewindows import  send_app_details
from utils.ipadress import get_ipaddress_info
from utils.sendversion import send_version
from utils.userlogginginfo import get_userlogging_info
from utils.screenshotconfig import screenshot_configuration
from utils.config_reader import version,interval_1,interval_2,interval_3,interval_4,interval_5,log_path




class Daemon:
    """
    A basic daemon class.
    Usage: subclass the Daemon class and override the run() method.
    """
    def __init__(self, pidfile):
        self.pidfile = pidfile

    token = ""

    def daemonize(self):
        """
        Do the UNIX double-fork magic to daemonize the process.
        """
        try:
            pid = os.fork() 
            if pid > 0:
                # Exit first parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write(f'Fork #1 failed: {err}\n')
            sys.exit(1)

        # Decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # Do second fork
        try:
            pid = os.fork() 
            if pid > 0:
                # Exit from second parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write(f'Fork #2 failed: {err}\n')
            sys.exit(1)

        # Write the pid file
        atexit.register(self.delete_pid)
        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f:
            f.write(pid + '\n')

    def delete_pid(self):
        os.remove(self.pidfile)

    async def start(self):
        """
        Start the daemon.
        """
        # Check for a pidfile to see if the daemon is already running
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
            print(f"Daemon already running under PID {pid}")
        except IOError:
            
            pass

        # Start the daemon
        self.daemonize()
        await self.run()

    def stop(self):
        """
        Stop the daemon.
        """
        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            print("pidfile does not exist. Daemon not running?")
            return

        # Try killing the daemon process
        try:
            while True:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            if "No such process" in str(err) and os.path.exists(self.pidfile):
                os.remove(self.pidfile)
            else:
                print(err)
                sys.exit(1)

    
    async def restart(self):
        """
        Restart the daemon.
        """
        self.stop()
        await self.start()

    def run(self):
        """
        Overwrite this method when you subclass Daemon.
        It will be called after the process has been daemonized.
        """

# Example of how to use the Daemon class
class MyDaemon(Daemon):

   async def run(self):
        # asyncio.run(monitor_idle_time())
        # loop = asyncio.new_event_loop()
        # asyncio_thread = threading.Thread(target=loop.run_until_complete, args=(monitor_idle_time(),))
        # asyncio_thread.start()

   
    # Setup logging
   
        # logging.basicConfig(filename=log_path, level=logging.INFO, 
        # format='%(asctime)s:%(levelname)s:%(message)s')


  
        # log_path = "/var/log/UserMonitor/"  # Directory where logs will be stored
        log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
        log_full_path = f"{log_path}/{log_filename}"

        

        # Create a rotating file handler
        file_handler = logging.handlers.TimedRotatingFileHandler(log_full_path, when='midnight', backupCount=15)  # Keep logs for 7 days
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        file_handler.setFormatter(formatter)

       # Add the file handler to the root logger
        logging.getLogger().addHandler(file_handler)

       # Set the logging level for the root logger
        logging.getLogger().setLevel(logging.INFO)

       # Log a message
        logging.info('Logging started.')
       
        await send_token()
        await screenshot_configuration()
        await send_version(version)

      

        
        counter=0

        while True:
            logging.info("Inside While")
            counter += 1
            logging.info(counter)


            now = datetime.now()
            if now.hour==0 and now.minute==0 and now.second==0:
             try:
                    await asyncio.gather(
                      send_token(),
                      screenshot_configuration(),
                      send_version(version)
                        
                    )
                    logging.info("first second of the day")
             except Exception as e:
                    logging.error(f"Error in Interval 3 block: {e}")


            if counter % interval_1 == 0:
               logging.info("Interval 1")
            if counter % interval_2 == 0:
                logging.info("Interval 2")

            if counter % interval_3 == 0:
                try:
                    await asyncio.gather(
                        send_app_details(),
                        get_system_info(),
                        get_ipaddress_info(),
                        get_userlogging_info(),
                      
                        
                    )
                    logging.info("Interval 3")
                except Exception as e:
                    logging.error(f"Error in Interval 3 block: {e}")

                
            if  counter % interval_4 == 0:
                logging.info("Interval 4")

            if  counter % interval_5 == 0:
                logging.info("Interval 5")
                counter = 0

            time.sleep(1)
        # while True:

        #     time.sleep(15)

        #     logging.info("Daemon is running")

        #     logging.info("IdleTime :"  + str(get_idle_time()) + "seconds")

        #     logging.info("ActiveApplications :" + str(await send_app_details()))

        #     logging.info("UserMetaData :"  + str(await get_system_info()))

        #     logging.info("IpInfo :"  + str(await get_ipaddress_info()))

        #     logging.info("UserloggingActivity :" + str(await get_userlogging_info()))
            
        # Optionally, stop the event loop and join the thread when done
        loop.call_soon_threadsafe(loop.stop)
   
        asyncio_thread.join()




   
if __name__ == "__main__":
    try:
        daemon = MyDaemon('/tmp/usermonitor.pid')
        
        if len(sys.argv) == 2:

            if 'start' == sys.argv[1]:
                 print("agent start")
                 asyncio.run(daemon.start())
            elif 'stop' == sys.argv[1]:
                print("agent stop")
                asyncio.run(daemon.stop())
            elif 'restart' == sys.argv[1]:
                asyncio.run(daemon.restart())
            else:
                print(f"Unknown command: {sys.argv[1]}")
                sys.exit(2)
            sys.exit(0)
        else:
            print("Usage: %s start|stop|restart" % sys.argv[0])
           
           
    except Exception as e:
        print("An error occurred:", str(e))