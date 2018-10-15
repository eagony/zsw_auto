# -*-coding: utf-8-*-
'''
author:fasico
start_time:10.11.18

'''
import time
import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    #读取文件
    try:
        with open('tk/ZGJDS_1.json','r',encoding='utf-8') as tk_json:
            tk = json.load(tk_json)
            
    except FileNotFoundError:
        print('file miss or broken!')
    
    username = 'your usename'
    password = 'your password.'

    try:
        browser = webdriver.Chrome('E:/chromedriver')
    except FileNotFoundError:
        print('webdriver not found!')

    try:
        browser.get('http://www.attop.com/wk/index.htm?id=74')
    except TimeoutException:
        print("Time out")
    finally:
        browser.find_element_by_class_name('Blue').click()
    try:
        #login
        browser.switch_to_frame('pageiframe')
        time.sleep(1)
        browser.find_element_by_id('username').send_keys(username)
        browser.find_element_by_id('password').send_keys(password)
        browser.find_element_by_id('rand').send_keys(input('verification code:'))
        browser.find_element_by_class_name('btn_logon').click()
        time.sleep(2)
        
    except NoSuchElementException:
        print('NoSuchElement!')

    for jid in tk.keys():#遍历目录
        try:
            browser.get('http://www.attop.com/wk/learn.htm?id=74&' + jid)
        except TimeoutException:
            print('Time out at :'+ jid)
        
        WebDriverWait(browser,10).until(EC.presence_of_all_elements_located)
        print('starting'+jid)
        for tx_id in tk[jid].keys():#遍历每章节所有问题
            #for ans in tk[jid][tx_id]:#遍历每道题的答案
            for each in list(range(1,6)):#遍历所有选项
                input_xpath = '//*[@id="' + tx_id + '"]/ul/li[' + str(each) + ']/input'                  
                WebDriverWait(browser,10).until(EC.presence_of_all_elements_located)
                time.sleep(0.5)
                try:
                    ans_input = browser.find_element_by_xpath(input_xpath)
                    value = int(ans_input.get_attribute('value'))
                    checked = ans_input.get_attribute('checked')
                    #匹配正确答案                    
                    if checked:
                        print(jid+'-'+tx_id+'-'+str(value))
                        tk[jid][tx_id].append(value)
                    else :
                        pass
                except NoSuchElementException:
                    pass
                    #print('---'+str(each)+'---')
                finally:
                    pass
    print(tk)
    with open('tk/ZGJDS_f.json','w',encoding='utf-8') as zf_json:
        zf_json.write(json.dumps(tk))
    print('compllete!')
    
    time.sleep(10)
    browser.close()
    
if __name__ == '__main__':
    main()
