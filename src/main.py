import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import random
from datetime import datetime
from io import open

# CHROME_PATH = '/usr/lib/chromium-browser/chromium-browser'
CHROMEDRIVER_PATH = '/usr/lib/chromium-browser/chromedriver'
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--user-data-dir=~/.config/chromium')
# chrome_options.add_argument("profile-directory=Profile 1")
# chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
# chrome_options.binary_location = CHROME_PATH



def random_time(time):
    rand = random.randint(0,5)
    return time + rand/5

def page_is_loading(driver):
    while True:
        x = driver.execute_script("return document.readyState")
        if x == "complete":
            return True
        else:
            yield False


# def save_cookie(driver, path):
#     cookies = driver.get_cookies()
#     pickle.dump(cookies, open(path, "wb"))

# chrome_options.add_experimental_option("detach", True)

def open_drive():
    url = driver.command_executor._url
    session_id = driver.session_id
    print("url: "+str(url))
    print("session_id: "+str(session_id))
    driver.get("https://web.whatsapp.com/")
#     print("Scan QR Code, And then Enter")
#     input()
    print("loading..............")

    while True:
        try:
            input_box_search = driver.find_element_by_xpath("//*[@id=\"side\"]/div[1]/div/label/div/div[2]")
            break
        except:
            print("..............")
            time.sleep(1)





def go_to_group(contact):
    input_box_search= driver.find_element_by_xpath("//*[@id=\"side\"]/div[1]/div/label/div/div[2]")
    input_box_search.clear()
    input_box_search.click()
    time.sleep(random_time(2))
    input_box_search.send_keys(contact)
    time.sleep(random_time(2))
    selected_contact = driver.find_element_by_xpath("//span[@title='" + contact + "']")
    selected_contact.click()
    # input()
    time.sleep(7)


def send_text(text):
    inp_xpath = '//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]'
    input_box = driver.find_element_by_xpath(inp_xpath)
    time.sleep(random_time(2))
    input_box.send_keys(text + Keys.ENTER)
    time.sleep(random_time(2))


def is_it_new(last_massages, text_message, message_time):
    if last_massages== None:
        return True
    # '11:43  10/30/2021'
    last_time = last_massages[-1][1]
    message_time_24= datetime.strptime(message_time,"%H:%M:%S %m/%d/%Y")
    last_time_24= datetime.strptime(last_time,"%H:%M:%S %m/%d/%Y")
    if message_time_24 < last_time_24:
        return False
    else:
        for m in last_massages:
            if text_message == m[2] and message_time==m[1]:
                return False
    return True


def create_bad_words_list():
    path = "/home/pi/whatsappbot/src/hurtfulwordshebrew.txt"
    file = open(path, 'r', encoding='utf-8')
    bad_words_list = []
    lines = file.readlines()
    for line in lines:
        bad_words_list.append(line.rstrip())
    return bad_words_list


bad_words_list = create_bad_words_list()
print(bad_words_list)

def warning(m, bad_word,contact):

    go_to_group(contact)
    text = "הודעה זדונית נשלחה על ידי *" + m[0].rstrip() + "*     , המילה הפוגעת שזוהתה: *" + bad_word + "*    . תוכן ההודעה: " + m[2]
    print(text)
    send_text(text)
    time.sleep(random_time(1))


def get_key(val):
    for key, value in child_warning_contact.items():
        if val == value:
            return key

    return "key doesn't exist"

def unread_usernames(last_massages, scrolls=100):
    messages = list()
    soup = BeautifulSoup(driver.page_source, "html.parser")
    auth = None
    complete_time= None
    for i in soup.find_all("div", class_="message-in"):
        text_message = None
        data_message = None
        message = i.find("span", class_="selectable-text")
        if message:
            message2 = message.find("span")
            if message2 :
                text_message =message2.text
                # messages.append(text)
        # data = i.find("copyable-text", class_="data-pre-plain-text")
        try:
            unsplited = str( i.find("span", class_="copyable-text").find("span").parent.parent.parent.attrs.get("data-pre-plain-text"))
            date = unsplited.split("[")[1].split("]")[0]
            split1 = date.split(", ")
            part1 = split1[0] + ":00 "
            part2 = split1[1]
            complete_time = part1 + part2
            time = date.split(",")[0]
            auth_temp =unsplited.split("]")[1].replace(":","")
            auth_temp=auth_temp[1:]


#             if str(time) not in auth_temp:
#                 auth = auth_temp
            auth = auth_temp
            if (is_it_new(last_massages, text_message, complete_time)):
                messages.append([auth, complete_time, text_message, 1])
        except:
            pass
    # messages = list(filter(None, messages))
    if(messages == None):
        last_massages[-1][3]=0
        return last_massages
    return messages



child_warning_contact = {'אורדרוקמן': 'ליעדי','יואב תמיר': 'ליעדי'}




driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

contact1="קבוצה ראשונה"
contact2 = "קבוצה שנייה"


messages1=None
messages2=None


open_drive()

go_to_group(contact1)
messages1 = unread_usernames(messages1,scrolls=10)


while True:
    go_to_group(contact2)

    messages2 = unread_usernames(messages2,scrolls=10)
    
    if messages1 and messages1[-1][3]:
        for m in messages1:
            text = "*" + str(m[0]) + ":* " + str(m[2])
            send_text(text)
            time.sleep(random_time(0))
            
        for m in messages1:
            for bad_word in bad_words_list:
                if bad_word in m[2]:
                    contact = child_warning_contact.get(m[0].rstrip())
                    print(str(contact))
                    warning(m, bad_word,contact)

    go_to_group(contact1)

    messages1 = unread_usernames(messages1,scrolls=10)
    if messages2 and messages2[-1][3]:

        for m in messages2:
            text = "*" + str(m[0]) + ":* " + str(m[2])
            send_text(text)
            time.sleep(random_time(0))
            
        for m in messages2:
            for bad_word in bad_words_list:
                if bad_word in m[2]:
                    print(str(m[0]))
                    contact = child_warning_contact.get(str(m[0]).rstrip())
                    print(str(contact))
                    warning(m, bad_word,contact)


# go_to_group(contact2)
# messages2 = unread_usernames(messages2,scrolls=10)
# for m in messages1:
#     text = "*" + m[0] + ":* " + m[2]
#     send_text(text)
#     time.sleep(random_time(1))
#
# go_to_group(contact1)
# messages1 = unread_usernames(messages1,scrolls=10)
# for m in messages2:
#     text = "*" + m[0] + ":* " + m[2]
#     send_text(text)
#     time.sleep(random_time(1))
# driver.quit()
