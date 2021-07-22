from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# from bs4 import BeautifulSoup
import time
import datetime
# import pyautogui
# import webbrowser

chrome = webdriver.Chrome("./driver/chromedriver.exe")

chrome.get("https://gportal.jaxa.jp/gpr/search?tab=1")
# html = chrome.page_source.encode('utf-8')
wait = WebDriverWait(chrome, 10)


LOGIN_ID = "yasuharu"
PASSWORD = "Fishing@l0g1"

def login_to_jaxa():
    #login dialog open
    login_button = wait.until(EC.element_to_be_clickable((By.ID,'btn_login')))
    login_button.click()
    
    #login
    elem_id = chrome.find_element_by_name("auth_account")
    elem_password = chrome.find_element_by_name("auth_password")
    elem_id.send_keys(LOGIN_ID)
    elem_password.send_keys(PASSWORD)

    ui_login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"auth_login_submit")))
    ui_login_button.click()
    
    print('Complete login!')

   
login_to_jaxa()

#GCOM-C open
select_tag=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="tree_sat"]/tbody/tr[1]/td[2]/span/span[1]')))
click = ActionChains(chrome).move_to_element(select_tag).click()
click.perform()

#LEVEL2 open
level_tag=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="tree_sat"]/tbody/tr[3]/td[2]/span/span[1]')))
click = ActionChains(chrome).move_to_element(level_tag).click()
click.perform()

#海洋圏　open
kaiyouken_tag=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="tree_sat"]/tbody/tr[4]/td[2]/span/span[1]')))
click = ActionChains(chrome).move_to_element(kaiyouken_tag).click()
click.perform()

#water_temp check
water_temp_check=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="tree_sat"]/tbody/tr[7]/td[1]/span')))
click = ActionChains(chrome).move_to_element(water_temp_check).click()
click.perform()


#期間指定タブ
span_tab=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="step_title2"]')))
click = ActionChains(chrome).move_to_element(span_tab).click()
click.perform()

#期間指定
target_date = datetime.datetime.now()-datetime.timedelta(days=1)
START=target_date.strftime("%Y/%m/%d")

span_start=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="start_date_1"]')))
span_start.clear()
span_start.send_keys(START)

span_end=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="end_date_1"]')))
span_end.clear()
span_end.send_keys(START)


#範囲指定タブ
expand_tab=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="step_title3"]')))
click = ActionChains(chrome).move_to_element(expand_tab).click()
click.perform()

legion_tab=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ui-id-14"]/span')))
click = ActionChains(chrome).move_to_element(legion_tab).click()
click.perform()

#範囲入力
# expand_max_lon=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="geo_top"]')))
# expand_max_lon.send_keys('45.64988528641494')
# expand_max_lat=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="geo_right"]')))
# expand_max_lat.send_keys('146.909179687504')

# expand_min_lon=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="geo_bottom"]')))
# expand_min_lon.send_keys('40.91904390461632')
# expand_min_lat=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="geo_left"]')))
# expand_min_lat.send_keys('138.9111328125022')

#地名指定
place_name=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="placename"]')))
place_name.send_keys('日本, 北海道')
map_ref=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="placename_search"]')))
click = ActionChains(chrome).move_to_element(map_ref).click()
click.perform()

#検索
search_button=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menu_3"]/div[2]/button')))
click = ActionChains(chrome).move_to_element(search_button).click()
click.perform()

# プロダクト全選択
# product_list_button=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="cb_list"]')))
# click = ActionChains(chrome).move_to_element(product_list_button).click()
# click.perform()

#プロダクトリスト表示まち
wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="list"]/tbody')))
print("waited tr")

#リストの行数取得
t_rows_num=len(chrome.find_elements_by_xpath("//*[@id='list']/tbody/tr"))

if t_rows_num>8:
    t_rows_num = 8

print(t_rows_num)

#GCOM-Cのデータだけ選択
for num in range(1,t_rows_num+1):
    inner_text=chrome.find_element_by_xpath(f"/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/div[3]/div[3]/div/table/tbody/tr[{num}]/td[4]").get_attribute("title")
    if "GCOM-C" in inner_text:
        dl_button=wait.until(EC.element_to_be_clickable((By.XPATH,f"/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/div[3]/div[3]/div/table/tbody/tr[{num}]/td[8]/button[1]")))
        dl_button.click()
        time.sleep(3)
        print(inner_text)

print("DL done!")

#DLしたファイルを指定フォルダに格納
import os

current_dir = os.getcwd()
dir_date = START.replace('/','')
data_dir = current_dir+"\\"+dir_date

print(current_dir)
print(dir_date)
print(data_dir)

if dir_date not in os.listdir(current_dir):
    os.mkdir(current_dir+"\\"+dir_date)
    print("made dir!")

#fileの移動DLー＞検索日のファイル
import shutil
dl_dir=r"C:\Users\rockf\Downloads"
print(dl_dir)
list_file_name=os.listdir(dl_dir)
print(list_file_name)
# shutil.move(dl_file,move_to)

#1行目のtd[4]がGCOM-Cを含んでいたら、ダウンロードボタンクリック
# for row in t_rows_num:
#     if chrome.find_elements_by_xpath("//*[@id='list']/tbody/tr[${row}]").text

# //*[@id="GC1SG1_202107200146C05810_L2SG_SSTDK_2000"]/td[4]



#ダウンロード依頼
# dl_button=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="btn_dl_sum"]')))
# click = ActionChains(chrome).move_to_element(dl_button).click()
# click.perform()

#データ変換依頼
# make_data_button=wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[25]/div[3]/div/button[1]/span')))
# click = ActionChains(chrome).move_to_element(make_data_button).click()
# click.perform()



#quit
# close_button=wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[10]/div[3]/div/button/span')))
# click = ActionChains(chrome).move_to_element(close_button).click()
# click.perform()

# chrome.close()
