from config import LOCAL_USERNAME 
import os, time
from fuzzywuzzy import process


def find_closest_match(title, directory):
    while True :
            # List all files in the directory
            files = os.listdir(directory)
            
            # Get the best match based on fuzzy matching
            matched_file, score = process.extractOne(title, files)
            
            if score > 75:  # You can adjust this threshold
                return matched_file, score
            
            time.sleep(2)

def find_from_downloads(title):

    download_dir = f'/home/{LOCAL_USERNAME}/Downloads'
    # self.random_sleep(15,20)
        
    matched_file, similarity_score = find_closest_match(title, download_dir)
    file_path = os.path.join(download_dir, matched_file)
    
    # Refresh the list of files in the directory to check the current state
    current_files = os.listdir(download_dir)
    
    # Check if the matching file (excluding .crdownload) is present in the directory
    if matched_file in current_files and ".crdownload" not in matched_file:
        print(f"Found and matched file: {file_path}")
        return download_dir, file_path, True
    else :
        if not matched_file  :
            return download_dir, file_path, False
        
        # Check for the .crdownload version of the matched file
        crdownload_file = matched_file + ".crdownload"
        if crdownload_file in current_files:
            print("File is still downloading, waiting for completion...")
        else:
            print("File not found or download might have failed.")
        
        time.sleep(3) 
        return download_dir, file_path, False

def find_from_ownpath(title):

    download_dir = os.getcwd()
    # self.random_sleep(15,20)
        
    matched_file, similarity_score = find_closest_match(title, download_dir)
    file_path = os.path.join(download_dir, matched_file)
    
    # Refresh the list of files in the directory to check the current state
    current_files = os.listdir(download_dir)
    
    # Check if the matching file (excluding .crdownload) is present in the directory
    if matched_file in current_files and ".crdownload" not in matched_file:
        print(f"Found and matched file: {file_path}")
        return download_dir, file_path, True
    else :
        if not matched_file  :
            return download_dir, file_path, False
        
        # Check for the .crdownload version of the matched file
        crdownload_file = matched_file + ".crdownload"
        if crdownload_file in current_files:
            print("File is still downloading, waiting for completion...")
        else:
            print("File not found or download might have failed.")
        
        time.sleep(3) 
        return download_dir, file_path, False 
        