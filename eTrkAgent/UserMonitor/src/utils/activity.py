from evdev import InputDevice, ecodes
import asyncio
import subprocess
import time
import datetime
import logging
import os

current_idle_time = 0
last_updated = 0

def update_idle_time():
    global current_idle_time
    global last_updated
    logging.info('calling update_idle-time method')
    try:
        login_time = get_logintime()  # Ensure this function returns a valid timestamp
        current_time = time.time()
        if current_idle_time == 0:
            idle_time = current_time - login_time
            current_idle_time = idle_time
        else:
            idle_time = current_time - last_updated
            if idle_time > 60:
                current_idle_time += idle_time
    except Exception as e:
        logging.info('Error occurred' + e)
    last_updated = current_time
    return None

def get_devices():
    try:
        output = subprocess.check_output(['ls -l /dev/input/by-path/ | grep -E \'mouse|kbd\' | awk \'{print $11 }\' | sed \'s/.\{3\}//\''], shell=True).decode()
        devlist = output.split()
        prefixed_list = ['/dev/input/' + element for element in devlist]
        #logging.info(prefixed_list)
        return prefixed_list
    except Exception as e:
        logging.error("no putput", e)
    return prefixed_list

async def monitor_device(device_path):
    if not os.path.exists(device_path):
        logging.info(f"Device path does not exist: {device_path}")
        return    
    try:
        device = InputDevice(device_path)
        logging.info(f'Monitoring device: {device.path}, {device.name}')
        async for event in device.async_read_loop():
            if event.type == ecodes.EV_KEY or event.type == ecodes.EV_REL:
                update_idle_time()
                logging.info(f"Current idle time is {current_idle_time} seconds")
    except Exception as e:
        logging.info('Exception ignored as that device ioctl may not be applicable' + device_path)
    return

async def monitor_idle_time():
    get_devices()
    # List of device paths; replace these with the correct device paths for your keyboard and mouse
    device_paths = get_devices()

    # Create tasks for each device
    tasks = [monitor_device(path) for path in device_paths]

    # Run the tasks concurrently
    await asyncio.gather(*tasks)

def task_exception_handler(task):
    try:
        task.result()
    except Exception as e:
        logging.error(f"Exception in task: {e}")

def get_current_user_and_login_time(user):
    try:
        # Run the 'who' command and get output
        output = subprocess.check_output([f'who | grep {user} '], shell=True).decode()

        # Parse the output
        for line in output.splitlines():
            parts = line.split()
            if len(parts) > 3:
                user = parts[0]
                login_time = ' '.join(parts[2:4])
                return user, login_time
        return None, None

    except Exception as e:
        # print(f"Error: {e}")
        return None, None

def convert_to_timestamp(login_time_str):
    # Parse the string into a datetime object
    login_time = datetime.datetime.strptime(login_time_str, "%Y-%m-%d %H:%M")

    # Convert to Unix timestamp
    timestamp = login_time.timestamp()
    return timestamp

def add_idle_minutes(timestamp, idle_minutes):
    # Add idle minutes to the timestamp
    new_timestamp = timestamp + idle_minutes * 60
    return new_timestamp

def add_idle_seconds(timestamp, idle_seconds):
    new_timestamp = timestamp + idle_seconds
    return new_timestamp

# Example usage

def get_logintime():
    current_user, login_time = get_current_user_and_login_time('kumaran')
    login_time_str = ''+login_time
    timestamp = convert_to_timestamp(login_time_str)
    #logging.info('returns current login time....' + str(timestamp))
    return timestamp

def get_idle_time():
    global last_updated, current_idle_time
    current_time = time.time()

    # Calculate the elapsed time since the last update
    elapsed_time = current_time - last_updated

    # If no event has occurred since the last update, add the elapsed time to idle time
    if elapsed_time > 60:
        return current_idle_time + elapsed_time
    else:
        return current_idle_time

# Run the main function
if __name__ == "__main__":
    asyncio.run(monitor_idle_time())