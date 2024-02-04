# Anti-Quishing Tool

## Overview

Hello, You! Welcome to the Anti-Quishing Tool. I created this tool to help SOC analysts investigate QR code-related issues. It was originally developed to scan email QR codes, but it can now be used to scan any QR code.


This is the first version of the 'anti-quishing.py' tool. While functional, keep in mind that I wrote it in a hurry, so there are many problems that will be fixed in the future.

## Installation

To install the Anti-Quishing tool, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/mahmoudelfawair/anti-quishing.git
    ```

2. Navigate to the tool's directory:

    ```bash
    cd anti-quishing
    ```

3. Install the required dependencies:

    ```bash
    python3 -m pip install -r requirements.txt
    bash pre-run.sh
    ```
## Usage 
```
$ python3 anti-quishing.py -h
        
usage: anti-quishing.py [-h] [-u URLSCAN_API_KEY] [-i IPINFO_TOKEN] [--undefang]

A tool for analyzing phishing email cases with QR codes

options:
  -h, --help            show this help message and exit
  -u URLSCAN_API_KEY, --urlscan URLSCAN_API_KEY
                        Specify your urlscan API key
  -i IPINFO_TOKEN, --ipinfo IPINFO_TOKEN
                        Specify your ipinfo token
  --undefang            Enable undefang mode. In undefang mode, the tool will process and display IPs
                        or URLs without defanging them. Exercise caution when using this option, as it
                        may expose raw and potentially harmful data.

Author: Mahmoud Elfawair

```

## Compatibility

Currently, the Anti-Quishing tool is designed to work on Linux environments. Please note that it may not be compatible with other operating systems.

Feel free to explore, contribute, and report any issues you encounter. I appreciate your interest in the tool, and I may release future versions to address any identified issues and introduce new features.

Happy investigating!

