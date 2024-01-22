from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from models.ipo_model import IPO
from credential_manager import Database
import time
import re

URL = "https://meroshare.cdsc.com.np"
BANK = ''
USERNAME = ''
PASSWORD = ''
CRN = ''
PIN = ''

KITTA = 30

class Scrap(webdriver.Chrome):
    
    def __init__(self,teardown=True):
        self.teardown = teardown
        self.options = webdriver.ChromeOptions()
        #self.options.add_argument("--headless")
        self.options.add_experimental_option("detach", True)
        #self.service = Service(executable_path=driver_path)
        self.service = Service()
        #driver = self(webdriver.Chrome(ChromeDriverManager().install()))
        super(Scrap,self).__init__(options=self.options,service=self.service)
        self.implicitly_wait(5)
        self.maximize_window()
        self.get(URL)
        
    def login(self,bank,username,password):
        dpSelection = self.find_element(by=By.CSS_SELECTOR,value = 'span[class="select2-selection__rendered"]')
        dpSelection.click()
        dpField = self.find_element(by=By.CSS_SELECTOR,value = 'input[class="select2-search__field"]')
        dpField.send_keys(bank)
        dpList = self.find_element(by=By.CSS_SELECTOR,value = 'li[class="select2-results__option select2-results__option--highlighted"]')
        dpList.click()
        #dpSelection.selectByIndex(0)
        
        usernameTag = self.find_element(by=By.CSS_SELECTOR,value = 'input[id="username"]')
        usernameTag.send_keys(username)
        passwordTag = self.find_element(by=By.CSS_SELECTOR,value = 'input[id="password"]')
        passwordTag.send_keys(password)
        loginButton = self.find_element(by=By.CSS_SELECTOR,value = 'button[class="btn sign-in"]')
        loginButton.click()

    def checkLogin(self):
        #print(self.current_url)
        if 'login' in str(self.current_url):
            return False
        return True
    
    def traverseToPage(self):
        page = self.find_element(by=By.CSS_SELECTOR,value = 'i[class="msi msi-asba"]')
        page.click()
    
    def getListOfAvailableIPOs(self):
        listOfIpoDivs = self.find_elements(by=By.CSS_SELECTOR,value='div[class="company-list"]')
        ipos = []
        for ipo in listOfIpoDivs:
            name = self.cleanString(ipo.find_element(by=By.CSS_SELECTOR,value='span[tooltip="Company Name"]').get_attribute('innerHTML').strip())
            subGroup = self.cleanString(ipo.find_element(by=By.CSS_SELECTOR,value='span[tooltip="Sub Group"]').get_attribute('innerHTML').strip())
            shareType = self.cleanString(ipo.find_element(by=By.CSS_SELECTOR,value='span[tooltip="Share Type"]').get_attribute('innerHTML').strip())
            shareGroup = self.cleanString(ipo.find_element(by=By.CSS_SELECTOR,value='span[tooltip="Share Group"]').get_attribute('innerHTML').strip())
            ipos.append(IPO(name,subGroup,shareType,shareGroup))
        return ipos

    def cleanString(self,str):
        return re.sub('(<|>|!|--+)+(?=.*[^<>!-]|$)',"",str).strip()
    
    def openShare(self,ipo,crn,pin):
        print('Open share FUnction')
        count_open_share = 0
        listOfIpoDivs = self.find_elements(by=By.CSS_SELECTOR,value='div[class="company-list"]')
        for ipoUnit in listOfIpoDivs:
            print('inside list')
            name = ipoUnit.find_element(by=By.CSS_SELECTOR,value='span[tooltip="Company Name"]').get_attribute('innerHTML')
            print(name)
            print(ipo.name)
            if ipo.name in name:     
                print(ipo.name)
                while count_open_share<3:
                    try:
                        applyBtn = ipoUnit.find_element(by=By.CSS_SELECTOR,value='button[class="btn-issue"]')                        
                        break
                    except:
                        count_open_share+=1
                if count_open_share == 3:
                    print("going next")
                    return
                if "Edit" in applyBtn.get_attribute('innerHTML'):
                    print('Edit Button')
                    return 
                elif "Apply" in applyBtn.get_attribute('innerHTML'):
                    print('Clicking Apply')
                    applyBtn.click()
                    self.fillShare(crn,pin)
                    time.sleep(4)
                
    def fillShare(self,crnNum,pin):
        bank = self.find_element(by=By.CSS_SELECTOR,value='select[id="selectBank"]')
        bank.click()
        bankOption = bank.find_element(by=By.CSS_SELECTOR,value='option[value][required]')
        bankOption.click()
        
        appliedKitta = self.find_element(by=By.CSS_SELECTOR,value='input[name="appliedKitta"]')
        appliedKitta.send_keys(KITTA)
        crn = self.find_element(by=By.CSS_SELECTOR,value='input[id="crnNumber"]')        
        crn.send_keys(crnNum)
        disclaimer = self.find_element(by=By.CSS_SELECTOR,value='input[id="disclaimer"]')
        disclaimer.click()
        time.sleep(1)
        submitBtn = self.find_element(by=By.CSS_SELECTOR,value='button[class="btn btn-gap btn-primary"][type="submit"] ')
        submitBtn.click()
        self.finalizeApply(pin)
                
    def finalizeApply(self,pin):
        transactionPin = self.find_element(by=By.CSS_SELECTOR,value='input[id="transactionPIN"]')
        transactionPin.send_keys(pin)
        time.sleep(1)
        applyBtn = self.find_element(by=By.CSS_SELECTOR,value='div[class="confirm-page-btn"] button[class="btn btn-gap btn-primary"][type="submit"]')
        applyBtn.click()

    def logout(self):
        count_logout = 0
        while(count_logout<50):
            try:
                logoutBtn = self.find_element(by=By.CSS_SELECTOR,value='a[tooltip="Logout"]')    
                break
            except:
                print('Error while Logout...')
                print('Retrying...')
                time.sleep(10)
                count_logout += 1
                continue
        logoutBtn.click()

    # Default exit function
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:                        
            self.quit()
            
    
bot = Scrap()
db = Database()
users = db.getUsers()
MAX_TRIES = 3

for user in users:
    count_open_share = 0
    loginTries = 0
    while 1:
        if loginTries > MAX_TRIES: 
            exit(0)
            break
        bot.login(user.dp,user.name,user.password)
        time.sleep(1)
        loginTries+=1
        
        if bot.checkLogin():
            break

    bot.traverseToPage()
    ipos = bot.getListOfAvailableIPOs()


    for ipo in ipos:
        #print(ipo.shareType)
        #print(ipo.shareGroup)
        if ('IPO' in ipo.shareType) and 'Ordinary Shares' in ipo.shareGroup  :
            #print('Found')
            #print('Name = ',ipo.name)
            while(count_open_share<50):
                print(count_open_share)
                try:
                    print('opening')
                    bot.openShare(ipo,user.crn,user.pin)
                    print('Opened')
                    break
                except :
                    print('Error while Opening Share...')
                    print('Retrying...')
                    time.sleep(10)
                    count_open_share += 1
                    continue
            
    time.sleep(2)
    bot.logout()
    time.sleep(1)        
bot.quit()
