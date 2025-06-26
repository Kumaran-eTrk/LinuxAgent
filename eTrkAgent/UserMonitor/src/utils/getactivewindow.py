import subprocess

def get_window_title():
    try:
        # Get the active window ID
        active_window_id = subprocess.check_output([
            "xdotool", 
            "search", "--onlyvisible", "--class", ".", 
            "getwindowname", "%@"
        ]).decode().split('\n')
        return active_window_id
    except subprocess.CalledProcessError:
        return "Failed to get active window."

# Run the main function
if __name__ == "__main__":
    title = get_window_title()
    print(get_window_title())

