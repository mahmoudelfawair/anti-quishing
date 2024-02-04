#!/usr/bin/env python3

from datetime import datetime
from defang import defang
from os import remove
from socket import gethostbyname


import argparse
import cv2
import json
import requests 
import sys
import subprocess

TMP_FILENAME = f"/tmp/qrcode_{str(datetime.now()).replace(' ', '_')}.png"

def parse_args():
    parser = argparse.ArgumentParser(prog='anti-quishing.py', description='A tool for analyzing phishing email cases with QR codes', epilog="Author: Mahmoud Elfawair")
    parser.add_argument('-u' ,'--urlscan', metavar='URLSCAN_API_KEY', type=str, help='Specify your urlscan API key')
    parser.add_argument('-i' ,'--ipinfo', metavar='IPINFO_TOKEN', type=str, help='Specify your ipinfo token')
    parser.add_argument('--undefang', action="store_true", help='Enable undefang mode. In undefang mode, the tool will process and display IPs or URLs without defanging them. Exercise caution when using this option, as it may expose raw and potentially harmful data.')

    return parser.parse_args()


def grab_screenshot():
    """
    Takes an screenshot and returns the saved file path
    """

    try:
        retcode = subprocess.call('scrot -s ' + TMP_FILENAME, shell=True)
        if retcode == 0:
            return TMP_FILENAME
    except OSError as e:
        sys.stderr.write('Execution failed: ' + e)


def get_content():
    """
    Gets the content or the url from the image and then deletes it 
    and returns the content or the url of the qrcode 
    """

    img = cv2.imread(TMP_FILENAME)
    
    det = cv2.QRCodeDetector()

    content, pts, st_code = det.detectAndDecode(img)

    remove(TMP_FILENAME)

    # print(str(type(st_code)))
    # if str(type(st_code))== "<class 'NoneType'>":
    if st_code is None:

        print("This doesn't seem like a QR code")
        print("\033[95mNOTE:\033[0m If you are sure that it is a QR code, try again")
        exit(-1)
    return content

def url_scan(url, key):
    """
    Uses urlscan.io API to gather OSINT about the url. (https://urlscan.io/docs/api/)
    """
    
    API_key = key

    headers = {'API-Key': API_key,'Content-Type':'application/json'}
    data = {"url": f"{url}", "visibility": "private"}
    response = requests.post('https://urlscan.io/api/v1/scan/',headers=headers, data=json.dumps(data))
    
    print("\n" + "\033[1;35;40m" + "#" * 20 + " URLScan Results " + "#" * 20 + "\033[0m" + "\n")


    # Add more if you want to ...  (https://urlscan.io/docs/api/)
    keys = ['message', 'result']
    for key in keys:
        if key in response.json():
            print(f"\033[95m{key}:\033[00m {response.json()[key]}")

def ip_info(ip, token):
    """
    Uses Ipinfo.io API to gather OSINT about the IP address of the domain we got. (https://ipinfo.io/developers)
    """

    response = requests.get(f"http://ipinfo.io/{ip}?token={token}")
    keys = ['hostname', 'city', 'region', 'country', 'org', 'timezone']

    print("\n" + "\033[1;35;40m" + "#" * 20 + " IPinfo Results " + "#" * 20 + "\033[0m" + "\n")

    for key in keys:
        if key in response.json():
            print(f"\033[95m{key}:\033[00m {response.json()[key]}")


if __name__ == '__main__':

    args = parse_args()

    grab_screenshot()

    if (content := get_content()).lower().startswith('http'):
        url = content
        ip = gethostbyname(content.split('://', 1)[1].split('/')[0])

        if not (args.undefang):
            print(f"\033[95mDefanged URL:\033[00m {defang(url)}")
            print(f"\033[95mDefanged IP:\033[00m {defang(ip, all_dots=True)}")

        else:
            print(f"\033[95mURL:\033[00m {url}")
            print(f"\033[95mIP:\033[00m {ip}")

        if args.urlscan:
            url_scan(url, args.urlscan)
        if args.ipinfo:
            ip_info(ip, args.ipinfo)

    else:
        print("The content of the QR code isn't a URL")
        print(f"\033[95mcontent:\033[00m {content}")


