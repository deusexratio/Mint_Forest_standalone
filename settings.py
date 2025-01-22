import os
import sys
from pathlib import Path

import requests


def get_actual_ua():
    url = 'https://capmonster.cloud/api/useragent/actual'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise requests.HTTPError


concurrent_tasks = 3
RETRY_ATTEMPTS = 10
relay_bridge_inbound_chain = 'Optimism'
bridge_min = 0.0004
bridge_max = 0.0008

HEADLESS = False
PROXY = True
SLOW_MO = None
# SLOW_MO = 600
USE_FIXED_VIEWPORTS = True
VIEWPORTS = [{"width": 1920, "height": 1080}, {"width": 1368, "height": 786}]
USER_AGENT = get_actual_ua()


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.absolute()

USER_FILES_FOLDER = os.path.join(ROOT_DIR, 'user_files')
PROFILES_PATH = os.path.join(ROOT_DIR, 'user_files', 'profiles.xlsx')
RESULTS_PATH = os.path.join(ROOT_DIR, 'user_files', 'results.xlsx')

# EXTENTION_IDENTIFIER = 'acmacodkjbdgmoleebolmdjonilkdbch' - this is id from the Chrome Store
EXTENTION_IDENTIFIER = 'lahkeclhdmcgcbaojamdgkdmhfbfgfof' # this is your actual local id
EXTENTION_VERSION = '0.93.11'
EXTENTION_PATH = os.path.join(USER_FILES_FOLDER, 'Rabby-Wallet-Chrome')
EXTENTION_PASSWORD = '12345678'
