from selenium import webdriver
import datetime
import time
import random
from selenium.webdriver.common.by import By
from sys import exit

def __refresh_keep_alive()->None:
    """
    Refresh the driver to prevent login timeout.
    """
    driver.get("https://cart.taobao.com/cart.htm")
    print("Refresh the driver to prevent login timeout...")
    time.sleep(random.randint(55,70))


def keep_login_and_wait()->None:
    """
    Keep refresh till set time is approaching.
    """
    print("There is still a long time to go before the time point of rush purchase. \n\
        Start regular refresh to prevent login timeout...")
    while True:
        current_time = datetime.datetime.now()
        if (buy_time_object - current_time).seconds > 180:
            __refresh_keep_alive()
        else:
            print("The time point of rush purchase is approaching.\n\
                Stop automatic refresh and prepare to enter the rush purchase stage...")
            break


def buy()->None:
    """
    Exe buy.
    """
    driver.get("https://cart.taobao.com/cart.htm")
    print("The shopping cart website has been opened.\n\
        Please scan the code and log in within 15 seconds...")
    
    time.sleep(15)

    while True:
        try:
            driver.find_element(value="J_SelectAll1").click()
            print("All items in the shopping cart have been selected...")
            break
        except:
            print("No Select All button found. The page may not be loaded yet.\n\
                Try again...")

    while True:
        now = datetime.datetime.now()
        if now >= buy_time_object:
            print("The rush time is approaching.\n\
                Start trying to execute the rush...")
            try:
                if driver.find_element(value="J_Go"):
                    driver.find_element(value="J_Go").click()
                    print("The settlement button has been clicked...")
                    click_submit_times = 0
                    while True:
                        try:
                            driver.find_element(by=By.LINK_TEXT,value='提交订单').click()
                            print("The Submit Order button has been clicked...")
                            break
                            
                        except Exception as ee:
                            print("No Order Submission button found. The page may not be loaded yet.\n\
                                Try again...")
                            click_submit_times = click_submit_times + 1
            except Exception as e:
                print(e)
                print("Failed or submitted successfully.\n\
                    The program will be closed...")
                time.sleep(3)
                break



if __name__ == '__main__':
    print("CODE:01 of Stargazing Pavilion 13  by willkyu")
    print("===========================")
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    BUY_TIME = input(f"Please enter the rush time in the format as follows {cur_time} :\n")
    buy_time_object = datetime.datetime.strptime(BUY_TIME, '%Y-%m-%d %H:%M:%S')
    print(f"The rush purchase time has been set to: {buy_time_object}")
    now_time = datetime.datetime.now()
    if now_time > buy_time_object:
        print("The rush purchase time has passed.\n\
            Please confirm whether the rush purchase time is filled incorrectly...")
        exit(0)

    print("Opening Chrome browser...")
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    driver = webdriver.Chrome(executable_path='chromedriver', options=option)

    driver.maximize_window()
    print("Chrome browser has been opened...")

    keep_login_and_wait()
    buy()
    exit(0)
