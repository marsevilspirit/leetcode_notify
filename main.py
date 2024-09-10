import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

username = "marevilspirit"
notify_head = "example"
notify_title = "LeetCode刷题提醒"
notify_icon = "/home/mars/utils/leetcode_logo.png"
notify_timeout = 8000

# 定义一个函数来生成消息
def generate_message(number):
    return f"你现在刷了{number}道题，继续保持。"

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service('/usr/bin/chromedriver')
    return webdriver.Chrome(service=service, options=chrome_options)
    # return webdriver.Chrome(service=service)

def wait_for_number(driver, xpath, timeout=30, poll_frequency=0.5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = driver.find_element(By.XPATH, xpath)
            number = element.text.strip()
            if number and number != '-':
                return number
        except (NoSuchElementException, StaleElementReferenceException):
            pass
        time.sleep(poll_frequency)
    return None

def send_notification(title, message, icon=None, timeout=None, head=None):
    command = ['notify-send']
    if icon:
        command.extend(['-i', icon])
    if timeout:
        command.extend(['-t', str(timeout)])
    if head:
        command.extend(['-a', str(head)])
    command.extend([title, message])
    subprocess.run(command)

def get_leetcode_number(url, xpath, max_retries=3, retry_delay=5):
    for attempt in range(max_retries):
        driver = setup_driver()
        try:
            driver.get(url)
            
            number = wait_for_number(driver, xpath)
            
            if number:
                return number
            else:
                logging.warning("Number not loaded in time")
        
        except Exception as e:
            error_message = f"Unexpected error occurred: {e}"
            logging.error(error_message)
        finally:
            driver.quit()
        
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
    
    logging.error("Failed to retrieve the number after all attempts")
    return None

if __name__ == "__main__":
    url = f"https://leetcode.cn/u/{username}/"
    xpath = "//span[@class='text-[30px] font-semibold leading-[32px]']"
    
    number = get_leetcode_number(url, xpath)
    if number:
        notify_message = generate_message(number)
        send_notification(notify_title, notify_message, notify_icon, notify_timeout, notify_head)
    else:
        send_notification("网络有问题", "网络有问题, 请检查网络连接", icon='/home/mars/utils/leetcode_logo.png', timeout=8000)
