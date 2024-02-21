#!/usr/bin/env python3

import os
import time
import subprocess
import requests
from zipfile import ZipFile
from rich.console import Console
from rich.panel import Panel

console = Console()


def show_panel():
    panel = Panel("[bold cyan]VpnWizard[/bold cyan]\nManage VPN Configurations with Ease", subtitle="[yellow]Author: Ömer ŞAYAK[/yellow]")
    console.print(panel)


def clear_screen():
    subprocess.call("clear", shell=True)

# def get_public_ip():
#     response = requests.get("http://ipinfo.io/json")
#     data = response.json()
#     return data.get("country")

def download_vpn_source(url, destination):
    print(f"Trying to download VPN configuration from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        zip_file_name = url.split("/")[-1]
        zip_file_path = os.path.join(destination, zip_file_name)
        extract_path = os.path.join(destination, zip_file_name.replace('.zip', ''))  # Create a unique directory for each zip
        os.makedirs(extract_path, exist_ok=True)
        with open(zip_file_path, 'wb') as zip_file:
            zip_file.write(response.content)
        with ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        os.remove(zip_file_path)  # Remove the zip file after extraction
        print("VPN configuration downloaded and extracted successfully.")
        return extract_path  # Return the path where files were extracted
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")
        return None

def password_check():
    url = "https://www.vpnbook.com/password.php?t=0.94148700%201693642130"
    print("Checking for VPN password update...")
    response = requests.get(url)
    if response.status_code == 200:
        file_name = "passwd.jpg"
        with open(file_name, "wb") as file:
            file.write(response.content)
        subprocess.call(["xdg-open", file_name])  # Use "open" instead of "xdg-open" on macOS
        print("VPN password updated.")
    else:
        print(f"Failed to fetch password. Status code: {response.status_code}")

    # if os.path.exists(file_name):
    #     os.remove(file_name)

def connect_to_vpn(vpn_dir_path):
    print(f"Looking for VPN configuration files in {vpn_dir_path}")
    for root, dirs, files in os.walk(vpn_dir_path):
        for vpn_file in files:
            if vpn_file.endswith(".ovpn"):
                vpn_file_path = os.path.join(root, vpn_file)
                print(f"Found VPN config: {vpn_file_path}")
                print(f"Connecting using: {vpn_file_path}")
                subprocess.call(f"sudo openvpn --config \"{vpn_file_path}\"", shell=True)
                print("VPN connection attempt finished.")
                return  # Assuming we want to connect using the first .ovpn file we find
    print("No suitable VPN configuration file found.")




if __name__ == "__main__":
    clear_screen()
    show_panel()
    print("vpnwizard is starting...")
    print("Only synchronized with VPNBook")
    time.sleep(1)

    vpn_files_path = os.path.join(os.environ["HOME"], "vpnwizard", "source")

    if os.path.exists(vpn_files_path):
        subprocess.call(f"rm -rf {vpn_files_path}", shell=True)
    os.makedirs(vpn_files_path, exist_ok=True)

    password_check()
    console.print("[bold cyan]Username: vpnbook[/bold cyan]")
    print("Setup completed. Please select a country by entering the corresponding number:")
    print("----------------------------------")

    countries = ["Poland", "Germany", "USA", "Canada", "France"]
    urls = {
        "Poland": "https://www.vpnbook.com/free-openvpn-account/vpnbook-openvpn-pl140.zip",
        "Germany": "https://www.vpnbook.com/free-openvpn-account/vpnbook-openvpn-de220.zip",
        "USA": "https://www.vpnbook.com/free-openvpn-account/vpnbook-openvpn-us1.zip",
        "Canada": "https://www.vpnbook.com/free-openvpn-account/vpnbook-openvpn-ca196.zip",
        "France": "https://www.vpnbook.com/free-openvpn-account/vpnbook-openvpn-fr231.zip"
    }

    try:
        for idx, country in enumerate(countries, start=1):
            print(f"{idx}) {country}")

        while True:
            choice = input("Enter the number of your choice (enter '0' to Ctrl+C): ")
            if choice == '0':
                print("Exiting vpnwizard...")
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(countries):
                selected_country = countries[int(choice) - 1]
                vpn_dir_path = download_vpn_source(urls[selected_country], vpn_files_path)
                if vpn_dir_path:
                    connect_to_vpn(vpn_dir_path)
                else:
                    print("Failed to establish VPN connection due to download error.")
                break
            else:
                print("Invalid choice, please enter a number from 1 to 5.")
    except KeyboardInterrupt:
        print("\nExiting vpneasy due to KeyboardInterrupt (Ctrl+C)...")
    print("Goodbye!")
