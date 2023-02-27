from selenium import webdriver
import datetime
import time
import random
from selenium.webdriver.common.by import By
from sys import exit

# ====  标识登录状态、重试次数 ====
MAX_LOGIN_RETRY_TIMES = 2

current_retry_login_times = 0
login_success = False

def __refresh_keep_alive():
    # 重新加载购物车页面，定时操作，防止长时间不操作退出登录
    driver.get("https://cart.taobao.com/cart.htm")
    print("刷新购物车界面，防止登录超时...")
    time.sleep(random.randint(55,70))


def keep_login_and_wait():
    print("当前距离抢购时间点还有较长时间，开始定时刷新防止登录超时...")
    while True:
        current_time = datetime.datetime.now()
        if (buy_time_object - current_time).seconds > 180:
            __refresh_keep_alive()
        else:
            print("抢购时间点将近，停止自动刷新，准备进入抢购阶段...")
            break


def buy():
    # 打开购物车
    driver.get("https://cart.taobao.com/cart.htm")
    print("已打开购物车网站 请在15秒内扫码登录...")
    
    time.sleep(15)

    # 点击购物车里全选按钮
    while True:
        try:
            driver.find_element(value="J_SelectAll1").click()
            print("已经选中购物车中全部商品 ...")
            break
        except:
            print("没发现全选按钮，可能页面还没加载出来，重试...")

    while True:
        now = datetime.datetime.now()
        if now >= buy_time_object:
            print("到达抢购时间，开始尝试执行抢购...")
            try:
                # 点击结算按钮
                if driver.find_element(value="J_Go"):
                    driver.find_element(value="J_Go").click()
                    print("已经点击结算按钮...")
                    click_submit_times = 0
                    while True:
                        try:
                            driver.find_element(by=By.LINK_TEXT,value='提交订单').click()
                            print("已经点击提交订单按钮")
                            break
                            
                        except Exception as ee:
                            # print(ee)
                            print("没发现提交订单按钮，可能页面还没加载出来，重试...")
                            click_submit_times = click_submit_times + 1
                            #time.sleep(0.1)
            except Exception as e:
                print(e)
                print("失败了或者提交成功，即将退出程序。")
                time.sleep(3)
                break



if __name__ == '__main__':
    print("淘宝抢购小工具 拾叁号观星阁Ver.  by willkyu")
    print("===========================")
    # ==== 设定抢购时间 （修改此处，指定抢购时间点）====
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    BUY_TIME = input(f"请输入抢购时间，格式如 {cur_time} :\n")
    buy_time_object = datetime.datetime.strptime(BUY_TIME, '%Y-%m-%d %H:%M:%S')
    print(f"已设置抢购时间为：{buy_time_object}")
    now_time = datetime.datetime.now()
    if now_time > buy_time_object:
        print("当前已过抢购时间，请确认抢购时间是否填错...")
        exit(0)

    print("正在打开chrome浏览器...")
    # 让浏览器不要显示当前受自动化测试工具控制的提醒
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    #windows
    #driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=option)
    #linux
    #driver = webdriver.Chrome(executable_path='assets/chromedriver', chrome_options=option)
    driver = webdriver.Chrome(executable_path='chromedriver', options=option)

    driver.maximize_window()
    print("chrome浏览器已经打开...")

    keep_login_and_wait()
    buy()
    exit(0)