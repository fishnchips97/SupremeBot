# Code By Erik Fisher, Andrew Nguyen, Ashley Harrison
from selenium import webdriver
from datetime import datetime, timedelta
import time
import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Item(object):
    section = ""
    description = ""
    color = ""
    size = ""
    keywords = []

class User(object):
    name = ""
    email = ""
    phoneNum = ""
    streetAddress = ""
    zipCode = ""
    creditCardNum = ""
    creditCardExpMonth = ""
    creditCardExpYear = ""
    creditCardCVV = ""
    itemToBeBought = Item()


    def __init__(self):
        response = ""
        while (response != "1") and (response != "2"):
            print("(1)Read CSV\n(2)Type input\n(q)Quit")
            # response = input()
            print("Defaulting to CSV... input won't quite work as well right now")
            response = "1"
            if response == "1":
                print("\nEnter filename in this directory    ex: filename.csv\n")
                print("Row1 Format: name,email,phoneNum,address,zip,cardNum,expMon,expYear,CVV")
                print("Row2 Format for item: size,section,description,color, other keywords")

                returningToStart = False
                while True:
                    filename = input()
                    if filename == "q":
                        print("Quitting...")
                        returningToStart = True
                        response = "q"
                        break
                    try:
                        open(filename)
                        break
                    except Exception as e:
                        print("File Not Found. Try again or quit (q)")
                if returningToStart:
                    continue

                with open(filename) as csvfile:
                    readerCSV = csv.reader(csvfile, delimiter=',')
                    row1 = next(readerCSV)

                    self.name = row1[0]
                    self.email = row1[1]
                    self.phoneNum = row1[2]
                    self.streetAddress = row1[3]
                    self.zipCode = row1[4]
                    self.creditCardNum = row1[5]
                    self.creditCardExpMonth = row1[6]
                    self.creditCardExpYear = row1[7]
                    self.creditCardCVV = row1[8]
                    row2 = next(readerCSV)
                    self.itemToBeBought.size = row2[0]
                    if len(row2) > 1:
                        self.itemToBeBought.section = row2[1]
                        self.itemToBeBought.description = row2[2]
                        self.itemToBeBought.color = row2[3]
                        if len(row2) > 4:
                            counter = 4
                            while(counter < len(row2)):
                                self.itemToBeBought.keywords.append(row2[counter])
                                counter += 1


            elif response == "2":
                print("Please type user info...")
                # Keyboard Input
                print("\nEnter Billing Name    ex: Johnny Appleseed")
                self.name = input()
                print("\nEnter Email           ex: email@website.com")
                self.email = input()
                print("\nEnter Phone Number    ex: 333 555 7777")
                self.phoneNum = input()
                print("\nEnter street address  ex: 123 Sesame Street")
                self.streetAddress = input()
                print("\nEnter Zip Code        ex: 90210")
                self.zipCode = input()
                print("\nEnter Credit Card #   ex: 1234 5678 1234 5678")
                self.creditCardNum = input()
                print("\nCard expiration month  ex: 02")
                self.creditCardExpMonth = input()
                print("\nCard expiration year   ex: 2020")
                self.creditCardExpYear = input()
                print("\nEnter Card CVV        ex: 123")
                self.creditCardCVV = input()
                print("\n\nEnter Item Section    ex: sweatshirts")
                self.itemToBeBought.section = input()
                print("\nItem Description       ex: Zip Up")
                self.itemToBeBought.description = input()
                print("\nEnter Item Color       ex: Black")
                self.itemToBeBought.color = input()
                print("\nEnter Item Size       ex: s")
                self.itemToBeBought.size = input()
            elif response == "q":
                print("Closing Program")
                quit()
            else:
                print("Try Again.\n(1)Read CSV\n(2)Type input\n(q)Quit")

    def formatForInput(self):
        self.phoneNum = self.phoneNum.replace(" ","")
        self.phoneNum = self.phoneNum[0:3] + " " + self.phoneNum[3:6] + " " + self.phoneNum[6:10]

        self.creditCardNum = self.creditCardNum.replace(" ","")
        self.creditCardNum = self.creditCardNum[0:4]+" "+self.creditCardNum[4:8]+" "+self.creditCardNum[8:12]+" "+self.creditCardNum[12:16]


def waitTillTime(year, month, day, hour, minute, second):
    timeToStart = datetime(year, month, day, hour, minute, second);
    secondsToWait = (timeToStart - datetime.now()).seconds
    print(f"{secondsToWait} seconds till launch...")
    time.sleep(secondsToWait);
def refresherTillDrop():
    itemNumberToCheck = 15
    firstlinkBefore = browser.find_elements_by_tag_name("a")[itemNumberToCheck].get_attribute("href")
    while True:
        browser.refresh()
        time.sleep(0.7)

        firstlinkAfter = browser.find_elements_by_tag_name("a")[itemNumberToCheck].get_attribute("href")

        if firstlinkBefore != firstlinkAfter:
            print("New Link! Starting Search")
            break
        print(f"Same Link First Link, Refreshing...")

def findItem():
    browser.get(f"http://www.supremenewyork.com/shop/all/{customer.itemToBeBought.section}");
    foundItemLink = False
    for keyword in customer.itemToBeBought.keywords:
        try:
            itemLink = browser.find_element_by_partial_link_text(keyword).get_attribute("href")
            browser.get(itemLink)
            foundItemLink = True
            break
        except:
            pass

    if not foundItemLink:
        allItemsWebElements = browser.find_elements_by_partial_link_text(customer.itemToBeBought.description)
        allColorWebElements = browser.find_elements_by_partial_link_text(customer.itemToBeBought.color)


        brokeOut = False
        for item in allItemsWebElements:
            for color in allColorWebElements:
                if item.get_attribute("href") == color.get_attribute("href"):
                    foundLink = item.get_attribute("href")
                    brokeOut = True
                    break
            if brokeOut:
                break
        try:
            browser.get(foundLink)
        except:
            print("Couldn't Find Item")
            quit()

def checkOut():

    try:
        browser.find_element_by_name("s").send_keys(f"{customer.itemToBeBought.size}\n")
    except:
        print("No size selector found.")

    try:
        browser.find_element_by_name("commit").click()
    except:
        print("Sold Out")
        quit()

    time.sleep(0.3)
    browser.find_element_by_link_text("checkout now").click()

    typeHere = browser.find_element_by_id("order_billing_name")
    typeHere.send_keys(f"{customer.name}\t"+
                        f"{customer.email}\t"+
                        f"{customer.phoneNum}\t"+
                        f"{customer.streetAddress}\t\t"+
                        f"{customer.zipCode}\t\t\t\t \t"+
                        f"{customer.creditCardNum}\t"+
                        f"{customer.creditCardExpMonth}\t"+
                        f"{customer.creditCardExpYear}\t"+
                        f"{customer.creditCardCVV}\t ")

    time.sleep(0.2)
    clickHere = browser.find_element_by_name("commit")
    clickHere.click()




# Read in Data
customer = User()
customer.formatForInput()

print("\nStarting Browser\n")
browser = webdriver.Chrome()
browser.get("http://www.supremenewyork.com/shop/all/")

#Wait to begin searching   24 hour time
waitTillTime(2018, 3, 1, 8, 0, 0)
refresherTillDrop()

startTime = time.time()

findItem()
checkOut()

endTime = time.time()
totalTime = endTime - startTime
print(f"It took {totalTime:.1f} seconds after refresh")



# Color/Style Names
# Heather Grey
# Red
# Black
# White
# Navy
# Moss Green
# Bright Orange
# Plum
# Cardinal
# Pale Lime
# Royal (blue)
# Pale Pink
