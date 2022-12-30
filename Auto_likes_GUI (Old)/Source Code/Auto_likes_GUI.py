from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Tk, Button, Frame
import time


def login(email, password, driver):
    
    login_url = 'https://yay.space/?modalMode=login'
    driver.get(login_url)
    time.sleep(3)

    while True:

        try:
            # フォームにメールアドレスを入力
            driver.find_element(By.NAME, 'email').send_keys(email)
            time.sleep(1)

            # フォームにパスワードを入力
            driver.find_element(By.NAME, 'password').send_keys(password)
            time.sleep(1)

            # ログインボタンを押す
            driver.find_element(By.CLASS_NAME, 'Button--icon-login').click()
            time.sleep(1)
            break

        except:
            driver.get(login_url)
            time.sleep(3)


    # ログインに成功したか判定するために現在のURLを取得する
    if driver.current_url != 'https://yay.space/':
        driver.quit()
        print('Error : ログインに失敗しました')
        messagebox.showerror('エラー', 'メールアドレス、もしくはパスワードが違います')
    else:
        print('ログインしました')


def press_likes(driver):
    
    # いいねをしていない投稿を探索
    find_post_to_like = "//div[not(contains(@class, 'Hot'))]/div/div/div/div/ul/li/a[contains(@class, 'PostActions__a') and contains(@class, 'PostActions__a--like') and not(contains(@class, 'active'))]"
    post_to_like = driver.find_element(By.XPATH, find_post_to_like)

    # いいねが可能かどうかを判定
    while True:
        if post_to_like.is_enabled():
            post_to_like.click()
            break
        else:
            time.sleep(1)


def automate_like(likes_cnt, driver):

    # タイムラインの設定
    tl_setting_url = 'https://yay.space/timeline?modalMode=tf'
    driver.get(tl_setting_url)
    time.sleep(3)

    #返信を非表示にする
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
            print('いいねした回数 : ' + str(i))

            if i % 30 == 0:
                driver.get(tl_url)
                time.sleep(3)
                
        except ElementClickInterceptedException:

            i -= 1
            e += 1
            driver.get(tl_url)
            print('Warning : ElementClickInterceptedException [' + str(e) + ']')
            
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
                    print('Warning : いいねの回数を制限されているため、5分後に再開します')
                    # 五分間停止
                    time.sleep(300)
                    driver.get(tl_url)
                    time.sleep(3)
                else:
                    e = 0
                    
        except NoSuchElementException:
            print('Warning : NoSuchElementException')
            driver.get(tl_url)
            time.sleep(3)
            
        except StaleElementReferenceException:
            print('Warning : StaleElementReferenceException')
            driver.get(tl_url)
            time.sleep(3)


def main(email, password, likes_cnt, driver):
    
    login(email, password, driver)

    automate_like(likes_cnt, driver)
    time.sleep(1)

    print('処理が完了しました！')
    driver.quit()

    messagebox.showinfo('確認', '処理が完了しました')


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def activate(minimize):
    
    driver = webdriver.Chrome('./chromedriver.exe')

    if len(username.get()) == 0 and len(get_password.get()) == 0:

        if len(like.get()) > 0 and is_int(like.get()):

            # 外部ファイルからメールアドレスとパスワードを取得
            with open('./email and password.txt', 'r') as f:
                text_file = f.read().split("\n")

            email = text_file[0]
            password = text_file[1]
            likes_cnt = int(like.get())

            if minimize:
                driver.minimize_window()

            main(email, password, likes_cnt, driver)

        else:

            messagebox.showerror('エラー', 'いいねの回数が入力されていません')
            return

        return

    elif len(username.get()) > 0 and len(get_password.get()) > 0:
        
        email = username.get()
        password = get_password.get()

        if len(like.get()) > 0 and is_int(like.get()):
            
            likes_cnt = int(like.get())
            
            if minimize:
                driver.minimize_window()
            time.sleep(1)

            main(email, password, likes_cnt, driver)

        else:

            messagebox.showerror('エラー', 'いいねの回数が入力されていません')
            return

    elif len(username.get()) > 0 and len(get_password.get()) == 0:

        messagebox.showerror('エラー', 'パスワードが入力されていません')
        return

    elif len(username.get()) == 0 and len(get_password.get()) > 0:

        messagebox.showerror('エラー', 'メールアドレスが入力されていません')
        return


# ブラウザを最小化するか判断するメソッド
def activate_with_minimize():
    activate(True)

def activate_without_minimize():
    activate(False)


if __name__ == '__main__':

    root = Tk()
    root.title('Yay! いいね自動化')
    root.resizable(False, False)
    frame1 = ttk.Frame(root, padding=(32))
    frame1.grid()

    label1 = ttk.Label(frame1, text='メールアドレス', padding=(5, 2))
    label1.grid(row=1, column=0, sticky=E)

    label2 = ttk.Label(frame1, text='パスワード', padding=(5, 2))
    label2.grid(row=2, column=0, sticky=E)

    label3 = ttk.Label(frame1, text='いいね回数', padding=(5, 2))
    label3.grid(row=3, column=0, sticky=E)

    username = StringVar()
    username_entry = ttk.Entry(
        frame1,
        textvariable=username,
        width=20)
    username_entry.grid(row=1, column=1)

    get_password = StringVar()
    get_password_entry = ttk.Entry(
        frame1,
        textvariable=get_password,
        width=20,
        show='*')
    get_password_entry.grid(row=2, column=1)

    like = StringVar()
    like_entry = ttk.Entry(
        frame1,
        textvariable=like,
        width=6)
    like_entry.grid(row=3, column=1)

    frame2 = ttk.Frame(frame1, padding=(0, 5))
    frame2.grid(row=5, column=1, sticky=W)

    button1 = ttk.Button(
        frame2, text='実行',
        command=activate_without_minimize)
    button1.pack(side=LEFT)

    minimize = ttk.Button(
        frame2, text='最小化して実行',
        command=activate_with_minimize)
    minimize.pack(side=LEFT)

    button2 = ttk.Button(
        frame2, text='キャンセル',
        command=root.destroy)
    button2.pack(side=LEFT)

    root.mainloop()
