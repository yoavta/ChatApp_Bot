import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import random
from datetime import datetime

# RASPBERRY PI SETTINGS
# # CHROME_PATH = '/usr/lib/chromium-browser/chromium-browser'
# CHROMEDRIVER_PATH = '/usr/lib/chromium-browser/chromedriver'
# WINDOW_SIZE = "1920,1080"
# chrome_options = Options()
# # chrome_options.add_argument("--headless")
# chrome_options.add_argument('--user-data-dir=~/.config/chromium')
# # chrome_options.add_argument("profile-directory=Profile 1")
# # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
# # chrome_options.binary_location = CHROME_PATH

# WINDOWS SETTINGS
CHROME_PATH = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
CHROMEDRIVER_PATH = 'C:/Users/tamir/OneDrive/PROJECTS/resources/chromedriver.exe'
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--user-data-dir=C:\\temp\\profile 1')
chrome_options.add_argument("profile-directory=Profile 1")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH


# main function
def main():
    run()


# generate random time
def random_time(time):
    rand = random.randint(0, 5)
    return time + rand / 5


# wait for page to reload
def page_is_loading(driver):
    while True:
        x = driver.execute_script("return document.readyState")
        if x == "complete":
            return True
        else:
            yield False


# open the driver and wait until the page is finished loading
def open_drive(driver):
    url = driver.command_executor._url
    session_id = driver.session_id
    print("url: " + str(url))
    print("session_id: " + str(session_id))
    driver.get("https://web.whatsapp.com/")
    print("loading..............")
    while True:
        try:
            input_box_search = driver.find_element_by_xpath("//*[@id=\"side\"]/div[1]/div/label/div/div[2]")
            time.sleep(1)
            break
        except:
            print("..............")
            time.sleep(1)


# go to specific group (or contact)
def go_to_group(driver, contact):
    input_box_search = driver.find_element_by_xpath("//*[@id=\"side\"]/div[1]/div/label/div/div[2]")
    input_box_search.clear()
    input_box_search.click()
    time.sleep(random_time(2))
    input_box_search.send_keys(contact)
    time.sleep(random_time(2))
    selected_contact = driver.find_element_by_xpath("//span[@title='" + contact + "']")
    selected_contact.click()
    # input()
    time.sleep(random_time(7))


# send text
def send_text(driver, text):
    inp_xpath = '//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]'
    input_box = driver.find_element_by_xpath(inp_xpath)
    time.sleep(random_time(2))
    input_box.send_keys(text + Keys.ENTER)
    time.sleep(random_time(2))


# check if that massage was already sent
def is_it_new(last_massages, text_message, message_time):
    if last_massages is None:
        return True
    last_time = last_massages[-1][1]
    #     message_time_24= datetime.strptime(message_time,"%H:%M:%S %m/%d/%Y")
    #     last_time_24= datetime.strptime(last_time,"%H:%M:%S %m/%d/%Y")
    print(message_time)
    message_time_24 = datetime.strptime(message_time, "%H:%M:%S %d.%m.%Y")
    last_time_24 = datetime.strptime(last_time, "%H:%M:%S %d.%m.%Y")

    if message_time_24 < last_time_24:
        return False
    else:
        for m in last_massages:
            if text_message == m[2] and message_time == m[1]:
                return False
    return True


# creating word list from hurtful word data base.
def create_bad_words_list():
    path = "C:\\Users\\tamir\\OneDrive\\PROJECTS\\whatsapp_bot\\src\\hurtfulwordshebrew.txt"
    file = open(path, 'r', encoding='utf-8')
    bad_words_list = []
    lines = file.readlines()
    for line in lines:
        bad_words_list.append(line.rstrip())
    return bad_words_list


# contact emergency_contact and send them a warning message.
def warning(driver, m, bad_word, contact):
    go_to_group(driver, contact)
    text = "הודעה זדונית נשלחה על ידי *" + m[
        0].rstrip() + "*     , המילה הפוגעת שזוהתה: *" + bad_word + "*    . תוכן ההודעה: " + m[2]
    print(text)
    send_text(driver, text)
    time.sleep(random_time(1))


def get_messages(driver, last_massages, scrolls=100):
    messages = list()
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for i in soup.find_all("div", class_="message-in"):
        text_message = None
        message = i.find("span", class_="selectable-text")
        if message:
            message2 = message.find("span")
            if message2:
                text_message = message2.text
                if text_message == "":
                    text_message = "רק אימוג'ים"

        try:
            unsplited = str(i.find("span", class_="copyable-text").find("span").parent.parent.parent.attrs.get(
                "data-pre-plain-text"))
            date = unsplited.split("[")[1].split("]")[0]
            split1 = date.split(", ")
            part1 = split1[0] + ":00 "
            part2 = split1[1]
            complete_time = part1 + part2
            auth_temp = unsplited.split("]")[1].replace(":", "")
            auth_temp = auth_temp[1:]
            auth = auth_temp
            if (is_it_new(last_massages, text_message, complete_time)):
                messages.append([auth, complete_time, text_message, 1])

        except:
            pass

    if last_massages is None and len(messages) == 0:
        return None
    if len(messages) == 0:
        last_massages[-1][3] = 0
        return last_massages

    return messages


def run():
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    bad_words_list = create_bad_words_list()
    child_warning_contact = {'אור דרוקמן': 'יואב תמיר', 'יואב תמיר': 'יואב תמיר'}
    contact1 = "קבוצה ראשונה"
    contact2 = "קבוצה שנייה"
    emergency_contact = 'יואב תמיר'
    messages1 = None
    messages2 = None
    open_drive(driver)
    go_to_group(driver, contact1)
    messages1 = get_messages(driver, messages1, scrolls=10)
    try:
        while True:
            go_to_group(driver, contact2)

            messages2 = get_messages(driver, messages2, scrolls=10)

            if messages1 and messages1[-1][3]:
                for m in messages1:
                    text = "*" + str(m[0]) + ":* " + str(m[2])
                    send_text(driver, text)
                    time.sleep(random_time(0))

                for m in messages1:
                    for bad_word in bad_words_list:
                        if bad_word in m[2]:
                            contact = child_warning_contact.get(m[0].rstrip())
                            print(str(contact))
                            try:
                                warning(driver, m, bad_word, emergency_contact)
                            except:
                                print("problem with warning")
            go_to_group(driver, contact1)

            messages1 = get_messages(driver, messages1, scrolls=10)
            if messages2 and messages2[-1][3]:

                for m in messages2:
                    text = "*" + str(m[0]) + ":* " + str(m[2])
                    send_text(driver, text)
                    time.sleep(random_time(0))

                for m in messages2:
                    for bad_word in bad_words_list:
                        if bad_word in m[2]:
                            print(str(m[0]))
                            contact = child_warning_contact.get(str(m[0]).rstrip())
                            print(str(contact))
                            try:
                                warning(driver, m, bad_word, emergency_contact)
                            except:
                                print("problem with warning")
    except Exception as error:
        print('Caught this error: ' + repr(error))
        driver.quit()


if __name__ == "__main__":
    main()
