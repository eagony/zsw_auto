# -*- coding: utf-8 -*- 
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
    #config
    username = '111111'
    password = '111111'
    course_id = '73'
    tk = {}
    tk_name = 'tk/MG.json'
    jids = [2033,2034,2035,2037,2038,2039,2040,2041,2042,2043,2044,2045,2046,2047,2049,2052,2096,2098,2099,2101,2103,2104,2105,2106,2107,2108,2109,2110,2111,2112,2113,2114,2115,2116,2117,2118,2119,2120,2121,2122]

    try:
        browser = webdriver.Chrome('E:/chromedriver')
    except FileNotFoundError:
        print('webdriver not found!')

    index_url = 'http://www.attop.com/wk/index.htm?id=' + course_id

    try:
        browser.get(index_url)
        time.sleep(2)
    except TimeoutException:
        print("Time out")

    try:
        #login
        browser.find_element_by_class_name('Blue').click()
        browser.switch_to_frame('pageiframe')
        time.sleep(1)
        browser.find_element_by_id('username').send_keys(username)
        browser.find_element_by_id('password').send_keys(password)
        browser.find_element_by_id('rand').send_keys(input('verification code:'))
        browser.find_element_by_class_name('btn_logon').click()
        time.sleep(2)
        
    except NoSuchElementException:
        print('NoSuchElement!')
    
    learn_url = 'http://www.attop.com/wk/learn.htm?id=' + course_id

    for jid in jids:

        try:
            browser.get(learn_url + '&jid=' + str(jid))
            print('starting: '+str(jid))
            time.sleep(3)
            WebDriverWait(browser,10).until(EC.presence_of_all_elements_located)
            xts = browser.find_elements_by_class_name('ed-ans')
            jid_id = 'jid=' + str(jid)
            tk[jid_id] = {}
            for xt in xts:
                id = xt.get_attribute('id')    
                tk[jid_id][id] = []
                for choice_id in list(range(1,6)):
                    choice_xpath = '//*[@id="' + id + '"]/ul/li[' + str(choice_id) + ']/input'
                    WebDriverWait(browser,10).until(EC.presence_of_all_elements_located)
                    try:
                        choice = browser.find_element_by_xpath(choice_xpath)
                        browser.execute_script('arguments[0].scrollIntoView(false);',choice)
                        checked = choice.get_attribute('checked')
                        if checked:
                            value = choice.get_attribute('value')
                            print('jid=' + str(jid)+'-'+id+'-'+ value)
                            tk[jid_id][id].append(int(value))

                        else:
                            pass
                    except:
                        break
        except:
            continue
        

    tk_json = json.dumps(tk,indent=4)
    print(tk_json)

    with open(tk_name,'w',encoding='utf-8') as newtk_json:
        newtk_json.write(tk_json)   
        newtk_json.close()    

    print('compllete!')
    
    time.sleep(10)
    browser.close()
    
if __name__ == '__main__':
    main()
