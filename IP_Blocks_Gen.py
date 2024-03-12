import requests
from time import time, sleep
from os import system as SYSTEM, remove # SYSTEM because we use system for platform.
from colorama import init, Fore, Style
import socket
import platform
import subprocess

def sort_ips(input_file, output_file):
    # Read IP ranges from input file
    with open(input_file, 'r') as file:
        ip_ranges = file.readlines()

    # Sort IP ranges
    sorted_ips = sorted(ip_ranges, key=lambda ip: tuple(map(int, ip.split('-')[0].split('.'))))

    # Write sorted IP ranges to output file
    with open(output_file, 'w') as file:
        file.writelines(sorted_ips)
    remove(input_file)

def clear_terminal():
    operating_system = platform.system()
    if operating_system == "Windows":
        # For Windows
        SYSTEM("cls")
    else:
        # For Linux, macOS, and others
        subprocess.call("clear", shell=True)

def check_internet_connection():
    try:
        clear_terminal()
        print(f"{Fore.GREEN}\n[ $ ] Checking Internet Connection...", sep="")
        sleep(1)
        # Attempt to connect to a well-known host
        socket.create_connection(("www.ipdeny.com", 80))
        return True
    except OSError:
        return False

# Initialize colorama
init()

# Main Def ( Get Result )
def create_acl_country_ip_range(country_code):
    url = f"http://ipdeny.com/ipblocks/data/countries/{country_code.lower()}.zone"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        ip_blocks = response.text.split("\n")
        ip_range = []
        for block in ip_blocks:
            if block:
                network, subnet = block.split("/")
                ip_range.append(network)
        with open(f"{country_code}_ip_range.txt", "w") as file:
            for i in range(len(ip_range)-1):
                file.write(ip_range[i] + "-" + ip_range[i+1] + "\n")
        sort_ips(f"{country_code}_ip_range.txt", f"{country_code}_ip_range_sorted.txt")
        print(f"{Fore.GREEN}[ $ ] IP Range Saved Successfully > {country_code}_ip_range_sorted.txt\n")
    except requests.exceptions.Timeout:
        print(f"\n{Fore.MAGENTA}", "=" * 60, sep="")
        print(f"{Fore.RED}\n[ Error ] Oops! Connection timed out while retrieving the IP range.\n{Style.RESET_ALL}\n{Fore.YELLOW}[ Solutions To The Problem ]\n[ 1 ] Check Internet Connection!\n[ 2 ] Check Your DNS ( IF YOU'RE USING )\n[ 3 ] Use VPN.")
    except requests.exceptions.RequestException:
        print(f"{Fore.RED}\n[ 404 Client Error ] Oops! Something went wrong while retrieving the IP range.\nWe Can't Find Country Code You Entered, Please Read {Fore.GREEN}CountryCode.txt{Fore.RED} OR Maybe We Don't Have It. :({Style.RESET_ALL}")

def menu():
    try:
        while True:
            clear_terminal()
            print(f"\n{Fore.MAGENTA}{"=" * 60}{Style.RESET_ALL}\n\n\t\t    {Fore.CYAN}IP Range Tool{Fore.WHITE}\n\n{Fore.MAGENTA}{"=" * 60}\n", sep="")
            code = input(f"{Fore.YELLOW}[ Code ] Enter Country Code ( in TXT file {Fore.RED}OR {Fore.BLUE}0{Fore.YELLOW} for Exit ): {Fore.LIGHTBLACK_EX}")
            if code == "0":
                exit()
            elif len(code) < 2:
                print(f"{Fore.RED}\n[ Error ] Please Enter Valid Country Code.")
                sleep(1)
                continue
            elif not code.isalpha() or len(code) != 2:
                print(f"{Fore.RED}\n[ Error ] Please Enter Valid Country Code.")
                sleep(1)
                continue
            else:
                pass
            start_time = time()
            print()
            print(f"{Fore.YELLOW}[ Get ] Processing...\n")
            create_acl_country_ip_range(code)
            end_time = time()
            print(f"\n{Fore.MAGENTA}", "=" * 60, "\n", sep="")
            print(f"{Fore.GREEN}[ $ ] Elapsed Time: {round(end_time - start_time, 2)} seconds{Style.RESET_ALL}")
            print(f"\n{Fore.MAGENTA}", "=" * 60, sep="")
            while True:
                user_choice = input(f"\n{Fore.YELLOW}Run Again? ( y / n ) : {Fore.LIGHTBLACK_EX}")
                if user_choice.lower() == 'y':
                    continue
                elif user_choice.lower() == 'n':
                    clear_terminal()
                    exit()
                else:
                    print(f"\n{Fore.RED}[ Error ] Invalid Input, Try Again!{Style.RESET_ALL}") 
                    sleep(1)
                    continue
    except Exception as e:
        print(f"{Fore.RED}\n\nAn unexpected error occurred.{Style.RESET_ALL}\n{Fore.GREEN}[ Error Message ]{Style.RESET_ALL}\n{e}")

if __name__ == '__main__':
    # Call the function to check internet connection
    is_connected = check_internet_connection()
    if is_connected:
        menu()
    else:
        print(f"{Fore.RED}\n\n\n[ Error ] Not Connected To The Internet, Please Check Connection And Try Again.", sep="")
        sleep(1.5)
        exit()
