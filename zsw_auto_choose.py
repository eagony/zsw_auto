#coding=utf-8
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

def elememt_exist(browser,url,xpath):
    exist = True
    browser.get(url)
    try:
        EC.invisibility_of_element((By.XPATH,xpath))
    except :
        exist = False
    finally:
        return exist

def main():
    #读取文件
    try:
        with open('tk/ZGJDS.json','r',encoding='utf-8') as tk_json, open('account.json','r',encoding='utf-8') as acc_json:
            tk = json.load(tk_json)
            account = json.load(acc_json)
            
    except FileNotFoundError:
        print('file miss or broken!')
    
    username = account['username']
    password = account['password']

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
        url = 'http://www.attop.com/wk/learn.htm?id=74&' + jid
        check_xpath = '//*[@id="showajaxinfo2"]/div/ul/li[3]/span[2]/a[1]'
        if elememt_exist(browser,url,check_xpath):            
            time.sleep(1)
            for tx_id in tk[jid].keys():#遍历每章节所有问题
                for ans in tk[jid][tx_id]:#遍历每道题的答案
                    for each in list(range(1,6)):#遍历所有选项
                        input_xpath = '//*[@id="' + tx_id + '"]/ul/li[' + str(each) + ']/input'                  
                        try:
                            ans_input = browser.find_element_by_xpath(input_xpath)
                            value = int(ans_input.get_attribute('value'))
                            checked = ans_input.get_attribute('checked')
                            #匹配正确答案                    
                            if value == ans and not checked:
                                browser.execute_script('arguments[0].scrollIntoView(false);',ans_input)
                                WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH,input_xpath))).click()
                                print(jid + '-' + tx_id + '-' + str(each) + '-done')
                                time.sleep(0.1)
                            else :
                                time.sleep(0.1)
                        except :
                            continue
                        finally:
                            pass
            #提交答案
            try:
                submit = browser.find_element_by_xpath('//*[@id="s2"]/a')
                submit.click()
                browser.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]').click()
            except :
                continue
        else:
            continue       
        
    print('all compllete!')
    time.sleep(3)
    browser.close()
    
if __name__ == '__main__':
    main()
