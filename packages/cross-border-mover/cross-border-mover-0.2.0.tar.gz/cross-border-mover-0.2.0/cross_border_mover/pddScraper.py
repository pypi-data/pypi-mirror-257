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
import pyautogui
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

    driver = webdriver.Chrome(options=chrome_options,service=service)

    driver.implicitly_wait(60)
    driver.set_window_size(1920, 1080)
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(0.2, 1.2))

    loginBtn = driver.find_element(By.CLASS_NAME,"phone-login")
    print(loginBtn)
    loginBtn.click()
    # loginInfo = { 'phoneNumber' : '17689947667',  'validCode': '' }

    if loginInfo is not None:
        if loginInfo['phoneNumber']:
            driver.find_element(By.ID, 'user-mobile').click()
            driver.find_element(By.ID, 'user-mobile').send_keys(loginInfo['phoneNumber'])
            driver.find_element(By.ID, 'code-button').click()
        else:
            driver.execute_script('alert("未配置登陆账号密码,请扫码登陆");')
            time.sleep(5)
            alert = driver.switch_to.alert
            alert.dismiss()

    Qzax7E1w = driver.find_element(By.CLASS_NAME,"Qzax7E1w")
    print(Qzax7E1w)
    Qzax7E1w.click()
    time.sleep(random.uniform(0.2, 1.2))
    colorList = []
    skuWrapper = driver.find_element(By.CLASS_NAME,"_3NXAWOJU")
    skuItemWrappers = skuWrapper.find_elements(By.CLASS_NAME,"_1XqP0nf5")
    sku_items = skuItemWrappers[0].find_elements(By.CLASS_NAME,"_1WyUf92E")
    print(sku_items)
    for skus_item in sku_items:
        styleStr = 'no img'
        try:
            skus_item.click()
            time.sleep(random.uniform(0.2, 1.2))
            imageWrapper = driver.find_element(By.CLASS_NAME,"nxbx3dAD")
            
            styleStr = imageWrapper.find_element(By.TAG_NAME,"img").get_attribute("src")
        except:
            print("NO image")
            
        url = 'no img url'
        if styleStr != 'no img':
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', styleStr)
            if type(urls) == list:
                url = urls[0]
                url = url.replace('w/300/q/70', 'w/1200/q/90')
        title = skus_item.find_element(By.TAG_NAME,"span").text
        print(title)
        colorList.append({"title":title,"url":url})    
    print(colorList)


    sizeList = []
    if len(skuItemWrappers) > 1: 
        sku_sizes = skuItemWrappers[1].find_elements(By.CLASS_NAME,"_1WyUf92E")
        for sku_size in sku_sizes:
            size_text = sku_size.find_element(By.TAG_NAME,"span").text
            sizeList.append(size_text)
    print(sizeList)

    return colorList,sizeList
    
