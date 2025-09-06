import os
import requests
from urllib.parse import urlparse

def fetch_and_save_image():
    """
    Prompts the user for an image URL, downloads the image, and saves it
    to a 'Fetched_Images' directory.
    """
    # Prompt the user for a URL
    url = input("Please enter the URL of the image you want to download: ")

    # Define the directory name
    directory_name = "Fetched_Images"
    
    # Create the directory if it doesn't exist
    try:
        os.makedirs(directory_name, exist_ok=True)
        print(f"Directory '{directory_name}' ensured.")
    except OSError as e:
        print(f"Error creating directory '{directory_name}': {e}")
        return

    # Extract or generate a filename
    parsed_url = urlparse(url)
    # The last part of the path is usually the filename
    filename = os.path.basename(parsed_url.path)
    if not filename:
        # If no filename is in the URL, create a default one
        filename = "downloaded_image.jpg"
    
    # Full path to save the file
    file_path = os.path.join(directory_name, filename)

    print(f"Attempting to download from: {url}")
    try:
        # Fetch the image with a timeout and stream enabled for larger files
        response = requests.get(url, stream=True, timeout=10)
        
        # Check for HTTP errors
        response.raise_for_status()
        
        # Save the image in binary write mode ('wb')
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        
        print(f"Success! Image saved as '{file_path}'")
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print("The server responded with an error.")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
        print("Could not connect to the URL. Please check your internet connection and the URL.")
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
        print("The request timed out. The server might be slow or the URL is invalid.")
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred: {e}")
    except Exception as e:
        print(f"An unknown error occurred: {e}")

if __name__ == "__main__":
    fetch_and_save_image()