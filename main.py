import os
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.common.exceptions import NoSuchElementException

HOW_MANY = int(input('How many comments you want to like (0-20):'))

while HOW_MANY > 20:
    print('Cant like more than 20 comments, please choose a smaller number!')
    HOW_MANY = int(input('How many comments you want to like (0-20):'))


options = webdriver.ChromeOptions()
options.add_argument('--log-level=3')
options.add_argument(f"--user-data-dir={os.getcwd()}\\profile")
mobile_emulation = {
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
options.add_experimental_option("mobileEmulation", mobile_emulation)
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
bot = webdriver.Chrome(options=options, executable_path=CM().install())
bot.set_window_position(0, 0)
bot.set_window_size(414, 936)

url_file = open('urls.txt', "r")
urls = url_file.readlines()


def doesnt_exist(bot, xpath):
    try:
        bot.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return True
    else:
        return False


for url in urls:
    print('--Liking comments for this post: ' + url)

    bot.get(url)

    if not doesnt_exist(bot, '//*[@id="main"]/div/div[1]/div[2]/div[2]/div[2]/div[2]/button'):
        time.sleep(1)
        bot.find_element_by_xpath(
            '//*[@id="main"]/div/div[1]/div[2]/div[2]/span').click()
        print('Closed pop ups')
    else:
        print('No pop up window.')

    # pause
    time.sleep(4)
    bot.find_element_by_xpath(
        '//*[@id="main"]/div/div[1]/div[1]/div/div[3]/div/div/div[1]/div').click()

    # click on comments
    time.sleep(1)
    bot.find_element_by_xpath(
        '//*[@id="main"]/div/div[1]/div[1]/div/div[3]/div/div/div[2]/div/div[2]').click()
    time.sleep(2)

    try:
        l_buttons = bot.find_elements_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/div')

        for l_button in l_buttons[:HOW_MANY]:
            l_button.click()
            time.sleep(1)

    except NoSuchElementException:
        print('Couldnt like, comments are disabled.')

print('FINISHED')
bot.quit()
