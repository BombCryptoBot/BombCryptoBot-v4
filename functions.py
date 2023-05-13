import base64
import binascii
import json
import os
import string
import random
import sys
import re
import time
import unidecode
import traceback
import tempfile
import cv2
import numpy as np
import math
import magic
import hashlib
import rsa
import io
import operator
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.Random import get_random_bytes
from requests import *
from uuid import getnode as get_mac
from glob import glob
from datetime import datetime
from datetime import timedelta
if os.name != "nt":
    from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from uuid import uuid4
from pathlib import Path
from datetime import datetime, timedelta
from time import sleep
from PIL import Image, ImageOps

pyautogui = None

def print_banner():
    print(" ___            _     ___               _       ___      _   ")
    print("| _ ) ___ _ __ | |__ / __|_ _ _  _ _ __| |_ ___| _ ) ___| |_ ")
    print("| _ \/ _ \ '  \| '_ \ (__| '_| || | '_ \  _/ _ \ _ \/ _ \  _|")
    print("|___/\___/_|_|_|_.__/\___|_|  \_, | .__/\__\___/___/\___/\__|")
    print("                              |__/|_|            Cluster v1.6.0\nhttps://thebotsociety.net\nhttps://discord.gg/BotSociety\n\n")

sqrt3 = np.sqrt(3)
sqrt5 = np.sqrt(5)

def get_random_string(length):
    letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(letters) for i in range(length))

def file_exists(path):
    return os.path.isfile(path)

def int_or_default(data, default=None):
    data = str(data)
    try:
        data = "".join([el for el in data if el.isdigit()])
        return int(data)
    except Exception:
        return default

def date_or_default(data, fmt="%d/%m/%Y", default=None):
    data = str(data)
    try:
        return datetime.strptime(data, fmt)
    except Exception:
        return default

def only_digits(data):
    data = str(data)
    return "".join([el for el in data if el.isdigit()])

def wait_ready_state_completed(driver, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(lambda driver:driver.execute_script('return document.readyState=="complete";'))
        return True
    except (TimeoutException, JavascriptException):
        pass
    return False

def switch_to_frame_by_xpath_if_exists(driver, xpath, timeout=10):
    try:
        if wait_for_element_by_xpath(driver, xpath, timeout):
            WebDriverWait(driver, timeout).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath)))
            wait_ready_state_completed(driver, timeout)
            return True
    except (NoSuchWindowException, NoSuchElementException, TimeoutException):
        pass
    return False

def scroll_to(driver, x, y):
    try:
        driver.execute_script(f"window.scrollTo({x}, {y})");
        return True
    except (Exception, JavascriptException):
        return False

def scroll_to_bottom(driver):
    scroll_to(driver, '0', '9999999999')

def scroll_to_top(driver):
    scroll_to(driver, '0', '0')

def scroll_to_element_by_xpath(driver, xpath):
    try:
        wait_ready_state_completed(driver)
        if check_exists_by_xpath(driver, xpath):
            ActionChains(driver).move_to_element(driver.find_element_by_xpath(xpath)).perform()
            return True
        return False
    except (Exception, MoveTargetOutOfBoundsException):
        return False

def scroll_to_element_by_css_selector(driver, css_selector):
    wait_ready_state_completed(driver)
    if check_exists_by_css_selector(driver, css_selector):
        ActionChains(driver).move_to_element(driver.find_element_by_css_selector(css_selector)).perform()
        return True
    return False

def check_exists_by_xpath(driver, xpath):
    try:
        wait_ready_state_completed(driver)
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False

    return True

def check_exists_by_css_selector(driver, css_selector):
    try:
        wait_ready_state_completed(driver)
        driver.find_element_by_css_selector(css_selector)
    except NoSuchElementException:
        return False
    return True

def wait_for_clickable_element_by_xpath(driver, xpath, timeout=15):
    try:
        wait_ready_state_completed(driver, timeout)
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return True
    except (TimeoutException, ElementNotInteractableException) as e:
        return False

def wait_for_clickable_element_by_css_selector(driver, css_selector, timeout=15):
    try:
        wait_ready_state_completed(driver, timeout)
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        return True
    except (TimeoutException, ElementNotInteractableException) as e:
        return False

def wait_for_element_by_xpath(driver, xpath, timeout=10):
    try:
        wait_ready_state_completed(driver, timeout)
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return True
    except TimeoutException:
        return False

def wait_for_element_by_css_selector(driver, css_selector, timeout=10):
    try:
        wait_ready_state_completed(driver, timeout)
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        return True
    except TimeoutException:
        return False

def is_visible_by_xpath(driver, xpath):
    return wait_for_visible_element_by_xpath(driver, xpath, 1)

def wait_for_visible_element_by_xpath(driver, xpath, timeout=10):
    try:
        wait_ready_state_completed(driver, timeout)
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return True
    except TimeoutException:
        return False

def is_visible_by_css_selector(driver, css_selector):
    return wait_for_visible_element_by_css_selector(driver, css_selector,1)

def wait_for_visible_element_by_css_selector(driver, css_selector, timeout=10):
    try:
        wait_ready_state_completed(driver, timeout)
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
        return True
    except TimeoutException:
        return False

def get_alert_if_exists(driver, click_on_accept=True):
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(), "Timed out waiting for PA creation confirmation popup to appear.")
        alert = driver.switch_to.alert
        alert_text = alert.text
        if click_on_accept == True:
            alert.accept()

        return {"exists": True, "text": alert_text}
    except (TimeoutException, NoAlertPresentException, JavascriptException):
        pass

    try:
        wait_for_element_by_css_selector(driver, "body")
        driver.find_elements_by_css_selector("body")

        return {"exists": False, "text": ""}
    except UnexpectedAlertPresentException:
        alert = driver.switch_to.alert
        alert_text = alert.text
        if click_on_accept == True:
            alert.accept()

        return {"exists": True, "text": alert_text}
    except (NoAlertPresentException, NoSuchWindowException, JavascriptException):
        return {"exists": False, "text": ""}

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

def get_chrome_drive(driver_path=None, extension=None, useragent=None, disableContent=False, disableSecurity=False, proxy=None, profile_path=None, headless=False):
    if driver_path is None:
        driver_path = '/usr/bin/chromedriver'

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-logging')
    options.add_argument('--disable-crash-reporter')
    options.add_argument('--log-level=3')
    options.add_argument('--window-size=1024,700')
    options.add_argument('--window-position=0,0')
    options.add_argument('--high-dpi-support=0')
    options.add_argument('--force-device-scale-factor=1')

    if headless:
        options.add_argument("--headless")

    if profile_path is not None:
        options.add_argument(f"user-data-dir={profile_path}")

    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    options.add_argument('disable-infobars')
    # options.add_argument('--disable-gpu')

    if disableSecurity:
        options.add_argument("--disable-web-security")

    if proxy != None:
        proxy = createChromeProxyPlugin(proxy['host'], proxy['port'], proxy['user'], proxy['pass'])
        options.add_extension(proxy)

    if (disableContent):
        prefs = {
            'profile.default_content_setting_values': {
                "cookies": 1,
                "images": 2,
                "javascript": 1,
                "plugins": 1,
                "popups": 2,
                "geolocation": 2,
                "notifications": 2,
                "auto_select_certificate": 1,
                "fullscreen": 2,
                "mouselock": 2,
                "mixed_script": 2,
                "media_stream": 2,
                "media_stream_mic": 2,
                "media_stream_camera": 2,
                "protocol_handlers": 1,
                "ppapi_broker": 2,
                "automatic_downloads": 2,
                "midi_sysex": 2,
                "push_messaging": 2,
                "ssl_cert_decisions": 1,
                "metro_switch_to_desktop": 2,
                "protected_media_identifier": 2,
                "app_banner": 2,
                "site_engagement": 2,
                "durable_storage": 2
            }
        }

        options.add_experimental_option('prefs', prefs)

    if useragent != None:
        options.add_argument("user-agent=" + useragent)

    if extension != None:
        options.add_extension(extension)

    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    # driver.set_window_size(1280, 800)

    return driver

def get_element_image(driver, xpath, y_offset = 0):
    element = driver.find_element_by_xpath(xpath)
    location = element.location
    size = element.size

    tmp = f"{tempfile.gettempdir()}/ss_{uuid4()}.png"
    driver.save_screenshot(tmp)

    x = location['x']
    y = location['y'] + y_offset
    w = size['width']
    h = size['height']
    width = x + w
    height = y + h

    im = Image.open(tmp)
    im = im.crop((int(x), int(y), int(width), int(height)))

    im.save(tmp)

    return tmp

def display_start(show_display=False):
    display = Display(visible=show_display, size=(960, 670))
    display.start()
    return display

def display_stop(display):
    display.stop()
    return True

def curl(url, data={}, method="GET", file='', jsonResponse=True, timeout=30, headers={}, public_key=None, private_key=None, extraData = None, tries=0):
    try:
        if public_key:
            data = {"data": encrypt_rsa(json.dumps(data), public_key)}

        if extraData:
            for key,val in extraData.items():
                data[key] = val

        if method == "GET":
            r = get(url, data=data, headers=headers, timeout=timeout)
        if method == "POST":
            if file != '':
                mime = magic.Magic(mime=True)
                files = {'file': (file['filename'], open(file['filepath'], 'rb'), mime.from_file(file['filepath']), {'Expires': '0'})}
                r = post(url, data=data, headers=headers, files=files, timeout=timeout)
            else:
                r = post(url, data=data, headers=headers, timeout=timeout)

        data = r.content

        if jsonResponse:
            if '{' in data.decode("utf-8"):
                data = json.loads(data.decode("utf-8"))
            else:
                data = decrypt(data.decode("utf-8"), private_key)

            if (int(data['server_date']) + 5) < time.time():
                data = {"status": False, "msg": "invalid_request", "code": 0}
        return data
    except:
        if tries <= 3:
            return curl(url, data, method, file, jsonResponse, timeout, headers, public_key, private_key, extraData, (tries+1))
        return {"status": False, "msg": "invalid_request", "code": 0}

def encrypt(data: dict, key) -> str:
    data_json_64 = base64.b64encode(json.dumps(data).encode('ascii'))
    try:
        key = binascii.unhexlify(key)
        iv = Random.get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_GCM, iv)
        encrypted, tag = cipher.encrypt_and_digest(data_json_64)
        encrypted_64 = base64.b64encode(encrypted).decode('ascii')
        iv_64 = base64.b64encode(iv).decode('ascii')
        tag_64 = base64.b64encode(tag).decode('ascii')
        json_data = {'iv': iv_64, 'data': encrypted_64, 'tag': tag_64}
        return base64.b64encode(json.dumps(json_data).encode('ascii')).decode('ascii')
    except:
        return ''

def decrypt(data: str, key) -> dict:
    try:
        key = binascii.unhexlify(key)
        encrypted = json.loads(base64.b64decode(data).decode('ascii'))
        encrypted_data = base64.b64decode(encrypted['data'])
        iv = base64.b64decode(encrypted['iv'])
        tag = base64.b64decode(encrypted['tag'])
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted = cipher.decrypt_and_verify(encrypted_data, tag)
        return json.loads(base64.b64decode(decrypted).decode('ascii'))
    except:
        return {}

def encrypt_rsa(data: str, public_key):
    h = SHA.new(data.encode("utf-8"))
    cipher = PKCS1_v1_5.new(public_key)
    return base64.b64encode(cipher.encrypt(data.encode("utf-8"))).decode("utf-8")

def decrypt_rsa(data: str, private_key):
    cipher = PKCS1_v1_5.new(private_key)
    sentinel = get_random_bytes(16)
    return json.loads(cipher.decrypt(base64.b64decode(data), sentinel))

def rmdir(directory):
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
    return True

def char_generator(message):
    for c in message:
        yield ord(c)

def get_image(image_location):
    img = cv2.imread(image_location)
    return img

def gcd(x, y):
    while(y):
        x, y = y, x % y
    return x

def decode_image(img_loc):
    img = get_image(img_loc)
    pattern = gcd(len(img), len(img[0]))
    message = ''
    for i in range(len(img)):
        for j in range(len(img[0])):
            if (i-1 * j-1) % pattern == 0:
                if img[i-1][j-1][0] != 0:
                    message = message + chr(img[i-1][j-1][0])
                else:
                    return message

def get_mac_address():
    return get_mac()

def get_chest_screenshots(btn, frame):
    offset1 = {
        'x': btn['x']-498,
        'y': btn['y']+171,
        'w': (btn['x']-498) + 290,
        'h': (btn['y']+171) + 34
    }
    offset2 = {
        'x': btn['x']-498,
        'y': btn['y']+312,
        'w': (btn['x']-498) + 290,
        'h': (btn['y']+312) + 34
    }
    sleep(5)
    gry = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.threshold(gry, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return True, get_text_box(frame[offset1["y"]:offset1["h"], offset1["x"]:offset1["w"]]),get_text_box(frame[offset2["y"]:offset2["h"], offset2["x"]:offset2["w"]])

def get_text_box(img):
    shape = img.shape
    img = 255*(img > 128).astype(np.uint8)
    coords = cv2.findNonZero(img) # Find all non-zero points (text)
    x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
    if (y-5 >= 0):
        y -=5
        h += 5
    if (x-5 >= 0):
        x -=5
        w +=5
    if (w+5 <= shape[1]):
        w +=5
    if (h+5 <= shape[0]):
        h+=5
    return img[y:y+h, x:x+w]

def detect_stam(bar_y, background):
    size = 0
    for key,y in enumerate(background[bar_y]):
        if y[0] in [108, 89, 86, 105, 134] and y[1] in [142, 120, 116, 139, 168] and y[2] in [191, 176, 183, 197, 214]:
            break
        else:
            size+=1
    return size

def press_esc_key():
    pyautogui.press("escape")
    return True