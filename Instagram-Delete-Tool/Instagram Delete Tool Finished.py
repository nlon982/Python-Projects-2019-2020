import time
from selenium import webdriver
import random

def get_random(time):
    return time + (random.randrange(-1, 1) * 0.1)


def output_list_to_file(a_list, log_file):
    log_file.write("start log\n")
    for item in a_list:
        log_file.write(str(item) + "\n")
    log_file.write("end log\n")
    

browser = webdriver.Chrome()
browser.implicitly_wait(5)
browser.get('https://www.instagram.com/')

input("press any key when you've logged in. The script will take you to your DM page")

dm_button = browser.find_element_by_xpath("//a[contains(@class, 'xWeGp')]")
dm_button.click()
time.sleep(4)


a_list = browser.find_elements_by_xpath("//a[contains(@class, '-qQT3 rOtsg')]")
a_list[0].click() # it seems once it's clicked, it does a recalculation?
a_list = browser.find_elements_by_xpath("//a[contains(@class, '-qQT3 rOtsg')]")

i = 5 #################################################################################################################### What index should it delete at (starting at 0)
first_pass = True
while True:
    try:
        if first_pass == True: # it's one out in the beginning, a quick and lazy fix
            a_list[i - 1].click()
            first_pass = False
        else:
            a_list[i].click() # click a new person
    except:
        print("ran out of people")
        break

    time.sleep(2)

    user_input = input("Please confirm to delete. Please press 'Y' for Yes, any other key for no") ####################### ONCE CONFIRMED WORKING 1) Delete this line 2) Uncomment next line
    #user_input = "Y"
    if user_input == "Y":
        i_button = browser.find_element_by_xpath('//button[@class="wpO6b ZQScA"]/*[name()="svg"][@aria-label="View Thread Details"]')
        i_button.click()
            
        time.sleep(get_random(3)) # time it takes to click 'delete chat' button. Note get_random randomizes up to 0.1 second either side.

        delete_chat_button = browser.find_element_by_xpath('//*[contains(text(), "Delete Chat")]').find_element_by_xpath('..')
        delete_chat_button.click()

        time.sleep(get_random(4)) # time it takes to click 'delete' button
        
        delete_button = browser.find_element_by_xpath("//button[contains(@class, 'aOOlW -Cab_   ')]")
        delete_button.click()
            
        time.sleep(get_random(7)) # buffer time

        
    a_list = browser.find_elements_by_xpath("//a[contains(@class, '-qQT3 rOtsg')]")
