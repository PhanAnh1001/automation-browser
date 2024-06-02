# new_account.py
import setting
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import time
from captcha import saveImage, sendQuestion

DELAY_FIND_HTML_SECOND = 5
DELAY_AFFTER_SUCESS_CREAT_SECOND = 10

GRID_CAPCHA_IMAGE_XPATH = '//*[@id="rc-imageselect-target"]/table/tbody/tr[1]/td[1]/div/div[1]/img'
# GRID_CAPCHA_IMAGE_XPATH = '/html/body/div/div/div[2]/div[2]/div/table/tbody/tr[1]/td[1]/div/div[1]/img'
GRID_CAPCHA_INSTRUCTION_XPATH = '//*[@id="rc-imageselect"]/div[2]/div[1]/div[1]/div'
# //*[@id="rc-imageselect"]/div[2]/div[1]/div[1]/div/strong
GRID_CAPCHA_CLICK_BASE_XPATH = '//*[@id="rc-imageselect-target"]/table/tbody/tr[%s]/td[%s]'

def create(proxy: str, userInformations: dict, threadIndex: int, loopIndex: int):
    if setting.config['thread']['isTest']: return 1

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-notifications')

    ## Proxy
    # if proxy: options.add_argument('--proxy-server=%s' % proxy)

    ## User Agent
    # ua = UserAgent(platforms='pc')
    # random_user_agent = ua.random
    # print(random_user_agent)
    # options.add_argument("--headless")
    # options.add_argument(f"--user-agent={random_user_agent}")

    ## Emulation
    # mobile_emulation = {
        # "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
        # "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
    
    # mobile_emulation = { "deviceName": "iPhone XR" }
    # options.add_experimental_option("mobileEmulation", mobile_emulation)

    if setting.config['chromeDriver']['undetected']['isActive']:
        ## Chrome driver undetected
        service = Service(service=Service(ChromeDriverManager().install()))
        driver = uc.Chrome(service=service, options=options)
    else:
        ## Chrome driver normal
        version = setting.config['chromeDriver']['normal']['version']
        os = setting.config['chromeDriver']['normal']['os']
        chrome_driver_path = './chrome-driver/version-%s/chromedriver_%s' % (version, os)
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)

    url = setting.configSecret['main_page']
    driver.get(url)

    # # Get user Agent with execute_script
    driver_ua = driver.execute_script("return navigator.userAgent")
    print(driver_ua)

    wait = WebDriverWait(driver, DELAY_FIND_HTML_SECOND)

    ## Modal 1 Not Us location
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal0Dialog"]/button'))).click() # close model location alert

    ## Modal 2

    # Mobile
    # wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[1]/div/div/button'))).click() # click create account icon
    
    # Web
    # wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/header/div[3]/div[1]/div/div[2]/div[1]/div[4]/div/button'))).click() # click create account icon
    signinDropBtXpath='/html/body/div[1]/header/div[3]/div[1]/div/div[2]/div[1]/div[4]/div/button'
    driver.execute_script("arguments[0].scrollIntoView(true);", wait.until(EC.visibility_of_element_located((By.XPATH, signinDropBtXpath))))
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, signinDropBtXpath))))

    # modal2CreateAccBtXpath='/html/body/div[6]/div/div/div[2]/div/div/div/button'
    modal2CreateAccBtXpath='//*[@id="modal1Dialog"]/div/button'
    driver.execute_script("arguments[0].scrollIntoView(true);", wait.until(EC.visibility_of_element_located((By.XPATH, modal2CreateAccBtXpath))))
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, modal2CreateAccBtXpath))))

    ## Modal 3
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="email"]'))).send_keys(userInformations['email'])
    # continueXpath ='/html/body/div[6]/div/div/div[2]/div/div/div/form/button[1]'
    continueXpath = '//*[@id="modal2Dialog"]/div/form/button[1]'
    wait.until(EC.element_to_be_clickable((By.XPATH, continueXpath))).click() # continue bt

    ## Modal 4
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="firstName"]'))).send_keys(userInformations['firstName'])
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="lastName"]'))).send_keys(userInformations['lastName'])
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="register_password"]'))).send_keys(userInformations['password'])

    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="biRegMonth"]/option[%d]' % (setting.config['birthDay']['month'] + 2)))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="biRegDay"]/option[%d]' % (setting.config['birthDay']['day'] + 2)))).click()

    # modal4JoinBtXpath = '/html/body/div[6]/div/div/div[2]/div/div/div[2]/form/button'
    modal4JoinBtXpath ='//*[@id="modal3Dialog"]/div[2]/form/button'
    driver.execute_script("arguments[0].scrollIntoView(true);", wait.until(EC.visibility_of_element_located((By.XPATH, modal4JoinBtXpath))))
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, modal4JoinBtXpath))))

    print('Start Try---------------')
    try:
        # Save Gid Capcha Image, instruction
        iframeXpath = '/html/body/div[9]/div[2]/iframe'
        wait.until(EC.visibility_of_element_located((By.XPATH, iframeXpath)))
        driver.switch_to.frame(driver.find_element(By.XPATH, iframeXpath))
        print('switch_to_frame------------')
        imageSrc = driver.find_element(By.XPATH, GRID_CAPCHA_IMAGE_XPATH).get_attribute('src')
        instruction = driver.find_element(By.XPATH, GRID_CAPCHA_INSTRUCTION_XPATH).text
        print('imageSrc %s' % imageSrc)
        print('instruction %s' % instruction)

        captchaResult = sendQuestion(instruction, saveImage(imageSrc, threadIndex, loopIndex))
        print('captchaResult: ', captchaResult)

        for idClick in captchaResult:
            clickCssPath = '#rc-imageselect-target td[role="button"][tabindex="%d"][class="rc-imageselect-tile"]' % (int(idClick) + 3)
            print('clickCssPath %s' % clickCssPath)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, clickCssPath))).click()
        
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="recaptcha-verify-button"]'))).click()
        isSuccess = True
    except Exception as e:
        if 'Message:' not in e:
            print('Exception--------')
            print(e)
            isSuccess = False
        else:
            isSuccess = True

    print('start sleep------------')
    time.sleep(DELAY_AFFTER_SUCESS_CREAT_SECOND)

    if isSuccess:
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, iframeXpath)))
            driver.switch_to.frame(driver.find_element(By.XPATH, iframeXpath))
            print('switch_to_frame_2------------Faill')
        except Exception:
            if isSuccess: isSuccess = True
        else: isSuccess = False

    # userInformations
    print('%s, %s, %s, %s, %s, %s' % (userInformations['email'], userInformations['password'], userInformations['firstName'], userInformations['lastName'], userInformations['birthDay'], userInformations['birthMonth']))
    # see name of new account
    # try:
    #     # time.sleep(DELAY_AFFTER_SUCESS_CREAT_SECOND)
    #     WebDriverWait(driver, DELAY_AFFTER_SUCESS_CREAT_SECOND).until(EC.visibility_of_element_located((By.XPATH, '//h1[contains(text(), %s)]' % userInformations['firstName'])))
    # WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="account_drop_trigger"]/span[contains(text(), %s)]' % userInformations['firstName'])))
    # except Exception as e:
    #     print(e)

    # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//h2[contains(text(), %s)]' % userInformations['firstName'])))
    # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="account_drop_trigger"]/span[contains(text(), %s)]' % userInformations['firstName'])))

    driver.close()
    # Fix error Errno 2] No such file or directory: '/Users/admin/Library/Application Support/undetected_chromedriver/undetected/chromedriver-mac-x64/chromedriver
    # By kill ghost process
    # driver.quit()
    # os.waitpid(driver.browser_pid, 0)
    # os.waitpid(driver.service.process.pid, 0)

    return isSuccess
