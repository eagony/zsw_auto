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

    course_id = input('course id:')
    course = {'74':'ZGJDS.json','39':'SX.json','40':'MY.json','73':'MG.json'}

    #read tk and accout
    try:
        with open('tk/'+course[course_id],'r',encoding='utf-8') as tk_json, open('account.json','r',encoding='utf-8') as acc_json:
            tk = json.load(tk_json)
            account = json.load(acc_json)
    except FileNotFoundError:
        print('file miss or broken!')
    
    username = account['username']
    password = account['password']

    try:
        browser = webdriver.Chrome('chromedriver')
    except FileNotFoundError:
        print('webdriver not found!')
        
    try:
        browser.get('http://www.attop.com/wk/index.htm?id=' + course_id)
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

    for jid in tk.keys():
        print('start %s'%(jid) )
        url = 'http://www.attop.com/wk/learn.htm?id=' + course_id + '&' + jid
        check_xpath = '//*[@id="showajaxinfo2"]/div/ul/li[3]/span[2]/a[1]'
        time.sleep(1.5)
        browser.get(url)
        #评价
        while(True):
            try:
                WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,'//span[text()="马上评价"] ')))
                time.sleep(2)
                evaluate_button = browser.find_element_by_xpath('//span[text()="马上评价"] ')
                time.sleep(0.5)
                browser.execute_script('arguments[0].scrollIntoView(false);',evaluate_button)
                time.sleep(0.5)
                evaluate_button.click()
                time.sleep(0.5)
                browser.switch_to_frame('pageiframe')#切换iframe
                browser.find_element_by_class_name('ping_btn_3').click()#点击好评
                time.sleep(0.5)
                browser.find_element_by_class_name('aui_state_highlight').click()#点击确认好评
                time.sleep(0.5)
                browser.switch_to_default_content()#关闭窗口
                close_buttons = browser.find_elements_by_class_name('aui_close')
                for close_button in close_buttons:
                    if close_button.is_displayed():
                        close_button.click
                time.sleep(0.5)
                browser.refresh()
                time.sleep(0.5)
            except:
                print('%s:evaluate complete'%(jid))
                break
        #刷题 
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
                                time.sleep(1)
                            else :
                                time.sleep(1)
                        except :
                            continue
                        finally:
                            pass
            #提交答案
            try:
                submit = browser.find_element_by_xpath('//*[@id="s2"]/a')
                browser.execute_script('arguments[0].scrollIntoView(false);',submit)
                submit.click()
                browser.find_element_by_xpath('/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]').click()
            except :
                continue
        else:
            continue       
        
    print('all compllete!')
    time.sleep(5)
    browser.close()
    
if __name__ == '__main__':
    main()
