from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


def login(email, password, driver):
    
    login_url = 'https://yay.space/?modalMode=login'
    driver.get(login_url)
    time.sleep(3)

    while True:

        try:

            driver.find_element(By.NAME, 'email').send_keys(email)
            time.sleep(1)

            driver.find_element(By.NAME, 'password').send_keys(password)
            time.sleep(1)
            
            driver.find_element(By.CLASS_NAME, 'Button--icon-login').click()
            time.sleep(1)
            break

        except:

            driver.get(login_url)
            time.sleep(3)

    cur_url = driver.current_url

    if cur_url != 'https://yay.space/':
        driver.quit()
        print('Error : Login failed')
    else:
        print('Successfully logged in!')


def press_likes(driver):
    
    post_to_like_path = "//div[not(contains(@class, 'Hot'))]/div/div/div/div/ul/li/a[contains(@class, 'PostActions__a') and contains(@class, 'PostActions__a--like') and not(contains(@class, 'active'))]"
    post_to_like = driver.find_element(By.XPATH, post_to_like_path)
    
    while True:
        if post_to_like.is_enabled():
            post_to_like.click()
            break
        else:
            time.sleep(1)


def automate_like(likes_cnt, driver):
    
    tl_set_url = 'https://yay.space/timeline?modalMode=tf'
    driver.get(tl_set_url)
    time.sleep(3)

    driver.find_element(By.XPATH, '//*[@id="modals"]/div[1]/div/div[2]/div[2]/div/div/div/div').click()
    time.sleep(1)

    tl_url = 'https://yay.space/timeline'
    driver.get(tl_url)
    time.sleep(3)

    i = 0
    e = 0

    while i < likes_cnt:

        try:
            press_likes(driver)
            i += 1
            time.sleep(1)
            print('Liked : ' + str(i))

        except ElementClickInterceptedException:
            
            i -= 1
            e += 1
            driver.get(tl_url)
            print('Warning : E.C.I. Exception [' + str(e) + ']')

            if e == 1:
                e_start = time.time()
            elif e == 3:
                e_mid = time.time()
                e_elapsed = e_mid - e_start
                if e_elapsed <= 20:
                    print(str(round(e_elapsed, 1)) + ' sec')
                else:
                    e = 0
            elif e >= 5:
                e_end = time.time()
                e_elapsed = e_end - e_start
                if e_elapsed <= 40:
                    print(str(round(e_elapsed, 1)) + ' sec')
                    print('Warning : Sleeping for 5 mins because of the request limit')
                    time.sleep(300)
                    driver.get(tl_url)
                    time.sleep(3)
                else:
                    e = 0
                    
        except NoSuchElementException:
            print('Warning : N.S.E.Exception')
            driver.get(tl_url)
            time.sleep(3)

        except StaleElementReferenceException:
            print('Warning : S.E.R.Exception')
            driver.get(tl_url)
            time.sleep(3)


def main(email, password, likes_cnt, driver):
    
    login(email, password, driver)

    automate_like(likes_cnt, driver)
    time.sleep(1)

    print('Done!')
    driver.quit()

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':

    print('Username : ')
    email = input()
    print('Password : ')
    password = input()
    print('Likes : ')
    likes_cnt = input()

    if likes_cnt.isdecimal():
        likes_cnt = int(likes_cnt)
    
    if len(likes_cnt) == 0:
        likes_cnt = 999999999999999
    
    print('Turn on headless mode? y/n : ')
    isHeadless = input()

    options = webdriver.ChromeOptions()

    if len(isHeadless) == 0 or isHeadless == 'Y' or isHeadless == 'y':
        options.add_argument('--headless')
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    if len(email) == 0 and len(password) == 0:

        with open('./email and password.txt', 'r') as f:
            text_file = f.read().split("\n")
        email = text_file[0]
        password = text_file[1]

        main(email, password, likes_cnt, driver)

    elif len(email) > 0 and len(password) > 0:
        if is_int(likes_cnt):
            if len(likes_cnt) == 0:
                likes_cnt == 99999999
            main(email, password, likes_cnt, driver)

    elif len(email) > 0 and len(password) == 0:
        print('Error : Invalid format or not entered')

    elif len(email) == 0 and len(password) > 0:
        print('Error : Invalid format or not entered')
        