from selenium import webdriver
from selenium.webdriver.common.by import By
import copy
import json

browser = webdriver.Chrome('chromedriver.exe')
browser.get('https://finans.mynet.com/borsa/hisseler/')

browser.maximize_window() #default olarak küçük ekran geliyordu, bu yüzden maximize ettik
myTable = browser.find_element(By.CLASS_NAME, "tbody-type-default") #html içinden class ismine göre çektik
rows = copy.copy(myTable.find_elements(By.TAG_NAME, "tr")) #referansı atamak için copy kullandık
mainObj = {}

def kayitlariGetir(size = 0):

    if(size == 0):
        size = len(rows) #değer verilmediyse tüm kayıtların gelmesi için

    for row in rows[:size]:

        obj = {}
        browser2 = webdriver.Chrome('chromedriver.exe')
        columns = row.find_elements(By.TAG_NAME, "td")
        value_name = columns[0].text.lower().replace(" ", "-") + "/"
        aTag = columns[0].find_element(By.TAG_NAME, "a")
        href = aTag.get_attribute("href")
        browser2.get(href)
        browser2.maximize_window()
        dataInfoContainer = browser2.find_element(By.CLASS_NAME, "data-info-ul-box-m")
        ulList = dataInfoContainer.find_elements(By.TAG_NAME, "ul")
        for ulRow in ulList:
            liList = ulRow.find_elements(By.TAG_NAME, "li")
            for liRow in liList:
                spanList = liRow.find_elements(By.TAG_NAME, "span")
                obj[spanList[0].text] = spanList[1].text


        mainObj[value_name] = copy.copy(obj)
        browser2.quit()

kayitlariGetir(3)

print(mainObj)

with open('web_scraping.json', 'w', encoding='utf-8') as f:
    json.dump(mainObj, f, ensure_ascii=False, indent=2)
