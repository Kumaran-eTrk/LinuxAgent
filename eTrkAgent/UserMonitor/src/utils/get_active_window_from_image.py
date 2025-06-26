import base64
import logging
import subprocess
import pytesseract
from PIL import Image
from io import BytesIO
from utils.config_reader import screenshot_path

def get_window_info_from_screenshot(image_path):
    try:
        img = Image.open(image_path)

        # Adjust the box coordinates to capture a larger portion of the title bar
        box = (0, 0, img.width, 800)  # Adjust the height (100 pixels in this example)
        title_area = img.crop(box)

        title_text = pytesseract.image_to_string(title_area)
        window_id_output = subprocess.check_output(["xdotool", "getactivewindow"]).decode().strip()
        title_output = subprocess.check_output(["xdotool", "getwindowname", window_id_output]).decode().strip()

        img_byte_array = BytesIO()
        title_area.save(img_byte_array, format='PNG')
        img_binary_data = img_byte_array.getvalue()

        return title_output, img_binary_data

    except Exception as e:
        print(f"An error occurred in binary data: {e}")
        logging.info(f"An error occurred: {e}")
        return None, None

if __name__ == "__main__":
    screenshot_path = screenshot_path
    title, screenshot_data = get_window_info_from_screenshot(screenshot_path)

   
