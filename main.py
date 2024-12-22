import os
import requests
from bs4 import BeautifulSoup
import shutil

def download_latest_dll(url, download_path):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the latest download link
    download_link = soup.find("a", text="Download")['href']
    file_name = os.path.basename(download_link)
    destination = os.path.join(download_path, file_name)

    # Check if the file is already downloaded
    if os.path.exists(destination):
        print(f"{file_name} is already downloaded. Checking for updates...")
        response = requests.head(download_link)
        remote_size = int(response.headers.get('Content-Length', 0))
        local_size = os.path.getsize(destination)
        if local_size == remote_size:
            print(f"{file_name} is already up-to-date.")
            return destination
        else:
            print(f"{file_name} is outdated. Updating...")

    print(f"Downloading {file_name}...")
    with requests.get(download_link, stream=True) as dl_response:
        with open(destination, "wb") as file:
            shutil.copyfileobj(dl_response.raw, file)
    print(f"Downloaded {file_name}.")

    return destination

def update_game_dlls(game_path, dll_path):
    if not os.path.isdir(game_path):
        print(f"Game path {game_path} does not exist. Skipping.")
        return

    for root, _, files in os.walk(game_path):
        for file in files:
            if file.lower() == os.path.basename(dll_path).lower():
                destination = os.path.join(root, file)
                print(f"Updating DLL at {destination}...")
                shutil.copy2(dll_path, destination)
                print(f"Updated DLL at {destination}.")

def main():
    base_download_folder = r"C:\\Users\\Julien\\Documents\\DLSS DLLs"
    os.makedirs(base_download_folder, exist_ok=True)

    urls = {
        "DLSS": "https://www.techpowerup.com/download/nvidia-dlss-dll/",
        "DLSS Frame Generation": "https://www.techpowerup.com/download/nvidia-dlss-3-frame-generation-dll/",
        "DLSS Ray Reconstruction": "https://www.techpowerup.com/download/nvidia-dlss-3-ray-reconstruction-dll/"
    }

    downloaded_dlls = {}

    for name, url in urls.items():
        print(f"Processing {name}...")
        downloaded_dlls[name] = download_latest_dll(url, base_download_folder)

    # Ask the user for the game path or use the default Steam library path
    game_path = input("Enter the path to your game directory (or your Steam library): ").strip()
    
    for dll_name, dll_path in downloaded_dlls.items():
        print(f"Updating games with {dll_name}...")
        update_game_dlls(game_path, dll_path)

if __name__ == "__main__":
    main()