import subprocess



def get_local_username():
    try:
        # Run the `whoami` command using subprocess to get the current username
        result = subprocess.run(['whoami'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check if the command was successful
        if result.returncode == 0:
            # Return the username, stripping any trailing whitespace or newline
            return result.stdout.strip()
        else:
            # If the command failed, return the error message
            return f"Error: {result.stderr.strip()}"
    
    except Exception as e:
        # Handle any exceptions that may occur and return the exception message
        return f"Exception occurred: {str(e)}"
    
APPLE_USERNAME="wande4er777@gmail.com"
APPLE_PASSWORD="Wanderer@1234"
# APPLE_USERNAME="remi@lascauxmedia.group"
# APPLE_PASSWORD="Salut@10!!"
# if get_local_username()
LOCAL_USERNAME = get_local_username()
if LOCAL_USERNAME == "rk" :
    HEADLESS=False
else :
    HEADLESS=True
SERVER_IP="http://15.164.187.251:8000/"
GOOGLE_EMAIL="pmyjtb7021"
GOOGLE_PASSWORD="Pmy#2020"
DOWNLOAD_DIR = f'/home/{LOCAL_USERNAME}/Downloads'