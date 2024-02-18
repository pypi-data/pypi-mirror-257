import random
import time
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
import shutil
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import pyautogui
import re     

def getSKUInfo(url, loginInfo):
    
    chromedriver_autoinstaller.install()
    chrome_path = shutil.which("chromedriver")
    service = Service(executable_path=chrome_path)
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--disable-javascript")

    driver = webdriver.Chrome(options=chrome_options,service=service)
    # driver = webdriver.Firefox()

    driver.implicitly_wait(30)
    driver.set_window_size(1920, 1080)
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(0.2, 1.2))
    # driver.execute_script("window.scrollBy(0,500)　")
    # time.sleep(1)
    loginBtn = driver.find_element(By.CLASS_NAME,"SecurityContent--loginBtn--28e5PZf")
    # print(loginBtn)
    loginBtn.click()
    # login_id = driver.find_element(By.ID,"fm-login-id")
    # login_password = driver.find_element(By.ID,"fm-login-password")

    # login_id.clear()
    # login_password.clear()
    if loginInfo is not None:
        if loginInfo['userName']:
            # time.sleep(random.uniform(0.2, 1.2))
            driver.find_element(By.ID, 'fm-login-id').click()
            # time.sleep(random.uniform(0.2, 1.2))
            driver.find_element(By.ID, 'fm-login-id').send_keys(loginInfo['userName'])
        if loginInfo['password']:
            # time.sleep(random.uniform(0.2, 1.2))
            driver.find_element(By.ID, 'fm-login-password').click()
            # time.sleep(random.uniform(0.2, 1.2))
            driver.find_element(By.ID, 'fm-login-password').send_keys(loginInfo['password'])
        else:
            driver.execute_script('alert("未配置登陆账号密码,请扫码登陆");')
            time.sleep(5)
            alert = driver.switch_to.alert
            alert.dismiss()
            
        
    # try:
    #     skuWrapper = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME,"skuWrapper")))
    # finally:
    #     print('finally==============')
    #     time.sleep(random.uniform(0.2, 1.2))
    # driver.find_element(By.CLASS_NAME, 'fm-button fm-submit password-login').click()

    skuWrapper = driver.find_element(By.CLASS_NAME,"skuWrapper")
    colorList = []
    skuItemWrappers = skuWrapper.find_elements(By.CLASS_NAME,"skuItemWrapper")
    sku_items = skuItemWrappers[0].find_elements(By.CLASS_NAME,"skuItem")
    # print(sku_items)
    for skus_item in sku_items:
        styleStr = 'no img'
        try:
            styleStr = skus_item.find_element(By.CLASS_NAME,"skuIcon").get_attribute("src")
        except:
            print("NO image")
            
        url = 'no img url'
        if styleStr != 'no img':
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', styleStr)
            if type(urls) == list:
                url = urls[0]
                url = url.replace('60x60q50', '1200x1200q90')
        title = skus_item.find_element(By.CLASS_NAME,"skuValueName").text
        # print(title , url)
        colorList.append({"title":title,"url":url})    
    # print(colorList)


    sizeList = []
    if len(skuItemWrappers) > 1: 
        sku_sizes = skuItemWrappers[1].find_elements(By.CLASS_NAME,"skuItem")
        for sku_size in sku_sizes:
            size_text = sku_size.find_element(By.CLASS_NAME,"skuValueName").text
            sizeList.append(size_text)
        
    # print(sizeList)
    # driver.quit()

    return colorList,sizeList


    
