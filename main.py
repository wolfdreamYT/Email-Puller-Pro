import os
import socket
import subprocess
import platform
import time
import ipinfo
import re

# Get your own token here https://ipinfo.io/ this token is just a placeholder, replace it with the real one after going to website.
ACCESS_TOKEN = 'YOUR_TOKEN_GOES_HERE'
handler = ipinfo.getHandler(ACCESS_TOKEN)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def extract_domain_from_email(email):
    try:
        return email.split('@')[1]
    except IndexError:
        return None

def resolve_domain_to_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def fetch_hostname(ip_address):
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except socket.herror:
        return "Unknown"

def get_geoip_location(ip_address):
    try:
        details = handler.getDetails(ip_address)
        return {
            "IP": details.ip,
            "Hostname": details.hostname or "Unknown",
            "City": details.city or "Unknown",
            "Region": details.region or "Unknown",
            "Country": details.country_name or "Unknown",
            "Location": details.loc or "Unknown",
            "Organization": details.org or "Unknown",
            "Postal": details.postal or "Unknown",
            "Timezone": details.timezone or "Unknown",
        }
    except Exception as e:
        print(f"Error fetching GeoIP data for {ip_address}: {e}")
        return {
            "IP": ip_address,
            "Hostname": "Unknown",
            "City": "Unknown",
            "Region": "Unknown",
            "Country": "Unknown",
            "Location": "Unknown",
            "Organization": "Unknown",
            "Postal": "Unknown",
            "Timezone": "Unknown",
        }

def fetch_isp_website(organization):
    try:
        if not organization or organization == "Unknown":
            return "Unknown"

        org_parts = organization.split()
        for part in org_parts:
            if '.' in part:
                return f"https://{part.lower()}"

        return f"https://{org_parts[0].lower()}.com"
    except Exception as e:
        print(f"Error fetching ISP website: {e}")
        return "Unknown"

def fetch_device_info(email):
    try:
        domain = extract_domain_from_email(email)
        if not domain:
            print("Invalid email format.")
            return None

        ip_address = resolve_domain_to_ip(domain)
        if not ip_address:
            print(f"Could not resolve domain {domain} to an IP address.")
            return None

        geoip_info = get_geoip_location(ip_address)
        isp_website = fetch_isp_website(geoip_info.get("Organization"))

        device_info = {
            "Email": email,
            "Domain": domain,
            "IP Address": ip_address,
            "GeoIP Info": geoip_info,
            "ISP Info": {
                "ISP": geoip_info.get("Organization"),
                "ISP Website": isp_website,
                "ISP Location": geoip_info.get("Location"),
            },
        }
        return device_info
    except Exception as e:
        print(f"Error fetching device info for {email}: {e}")
        return None

def display_ascii_art():
    art = """
            ██████████████████████████████████████████████████████████████████████████████████████████████████████████████
            █▌ _____ __  __    _    ___ _       ____  _   _ _     _     _____ ____    ____  ____   ___   __     ______  ▐█
            █▌| ____|  \/  |  / \  |_ _| |     |  _ \| | | | |   | |   | ____|  _ \  |  _ \|  _ \ / _ \  \ \   / /___ \ ▐█
            █▌|  _| | |\/| | / _ \  | || |     | |_) | | | | |   | |   |  _| | |_) | | |_) | |_) | | | |  \ \ / /  __) |▐█
            █▌| |___| |  | |/ ___ \ | || |___  |  __/| |_| | |___| |___| |___|  _ <  |  __/|  _ <| |_| |   \ V /  / __/ ▐█
            █▌|_____|_|  |_/_/   \_\___|_____| |_|    \___/|_____|_____|_____|_| \_\ |_|   |_| \_\\___/     \_(_)|_____| ▐█
            ██████████████████████████████████████████████████████████████████████████████████████████████████████████████
    """
    print(f"\033[92m{art}\033[0m")

def main():
    while True:
        clear_console()
        display_ascii_art()

        email = input("\033[92mEnter email address: \033[0m").strip()

        if not validate_email(email):
            print("\033[91mInvalid email address. Please use a valid email format (e.g., user@example.com).\033[0m")
            time.sleep(2)
            continue

        info = fetch_device_info(email)
        if info:
            clear_console()
            display_ascii_art()
            print("\033[92mEmail Domain Info:\033[0m")
            for key, value in info.items():
                if isinstance(value, dict):
                    print(f"\033[92m{key}:\033[0m")
                    for sub_key, sub_value in value.items():
                        print(f"  {sub_key}: {sub_value}")
                else:
                    print(f"{key}: {value}")

        input("\033[93m\nPress Enter to restart...\033[0m")

if __name__ == "__main__":
    main()
