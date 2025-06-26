import asyncio
import os
from pathlib import Path
import subprocess
import logging
import time
def take_screenshot(filename):
    try:
        # _path=str(Path(__file__).parent)+filename

        # Command to take a screenshot
        # # w flag is important; it takes the active screen instead of the whole screen
        subprocess.getstatusoutput("flameshot full -r > "+filename)
        
        
        return  "Success"
    
    except Exception as e:
        logging.error(f"An error occurred in taking screenshots: {e}")
        return "false"

# Run the main function
if __name__ == "__main__":
     take_screenshot()
     
