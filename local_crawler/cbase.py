# shttps://www.guru99.com/chrome-options-desiredcapabilities.html

import json

import re
import selenium
import logging
#import pandas
import platform
import os
import pandas as pd

from selenium.webdriver.support import expected_conditions as EC 

from selenium.webdriver.chrome.options import Options
######## for cbase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement as WE ## type annotation


from log import customed_logger


class cbase():
    def __init__(self,path=None,chrome_version=108, headless=False):
        self.logger=customed_logger('CRAWLER','./local_crawler/log/').logger
        self.logger.info('init crawler')
        chrome_options = Options()
        if headless==True:
            chrome_options.add_argument('--headless')
            
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280x1696')
        # chrome_options.add_argument('--user-data-dir=/tmp/user-data')
        # chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--log-level=0')
        # chrome_options.add_argument('--v=99')
        # chrome_options.add_argument('--single-process')
        # chrome_options.add_argument('--data-path=/tmp/data-path')
        # chrome_options.add_argument('--ignore-certificate-errors')
        # chrome_options.add_argument('--homedir=/tmp')
        # chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
        # chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

        #chrome_options.binary_location = "/opt/python/bin/headless-chromium"
        
        
        if path ==None:
            _path = os.path.join(os.getcwd(),'local_crawler','src')
            
        if platform.platform().startswith('mac'):
            print("macOS call")
            target_string="chromedriver_mac"
        elif platform.platform().startswith('Linux') or platform.platform().startswith('linux') :
            print("linux")
            target_string="chromedriver_linux"
        
        target_string=f"{target_string}_{chrome_version}"
        
        _path = os.path.join(_path,target_string)
        self.driver = webdriver.Chrome(_path,chrome_options=chrome_options)
    '''
    functions for single action
    - check loading
    - check_depth
    - activate_depth
    - activate_href_with_card
    '''
    def check_loading(self,target):
        '''
        waiting a single item.
        '''
        try:
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,target)))
            self.logger.info(f"[check_loading]1st depth: checking health done.")
        except: 
            self.logger.error(f"[check_loading]1st depth:  checking health error.")
    def check_depth(
        self,
        checker,
        depth_level:int=None,
        before_info:pd.DataFrame=None,
        card:dict=None        
        ):
        '''
        checking single depth
        '''
        list_items=self.driver.find_elements(By.CLASS_NAME,checker)        
        list_items_decoding=[]
        depth_level = 1 if depth_level == None else depth_level
        n=0
        str=""
        if depth_level == 1:
            for i in list_items:
                '''
                
                '''
                ## for information
                strs=""
                strs=f"{strs} {i.get_attribute('innerHTML')}"
                str=i.get_attribute('innerHTML')
                cleaned_str=re.sub(r'<[/a-z,A-Z]+>',"",str)
                n+=1
                ## getter
                if card is None:
                    dicts={
                        f"order_{depth_level}" : n,
                        f"element_title_{depth_level}" : i.get_attribute('title'),
                        f"element_name_{depth_level}" : i.get_attribute('innerHTML'),
                        f"element_href_{depth_level}"  : i.get_attribute('href'),
                        f"element_class_{depth_level}" : i.get_attribute('class'),
                    }
                else:
                    dicts=dict()
                    for kk in card.keys():
                        case=card[kk].split("_")
                        if case[0]=="tag":
                            try:
                                self.logger.debug(f"[check_depth] : {case[0]}")
                                str=i.find_element(By.TAG_NAME,case[1]).get_attribute(case[-1])
                            except:
                                str=None
                                self.logger.info(f"[check_depth] {kk} : No string")
                        elif case[0]=="class":
                            try:
                                self.logger.debug(f"[check_depth] : {case[0]}")
                                str=i.find_element(By.CLASS_NAME,case[1]).get_attribute(case[-1])
                            except:
                                str=None
                                self.logger.info(f"[check_depth] {kk} : No string")
                        elif case[0]=="XPATH":
                            try:
                                self.logger.debug(f"[check_depth] : {case[0]}")
                                str=i.find_element(By.XPATH,case[1]).get_attribute(case[-1])
                            except:
                                str=None
                                self.logger.info(f"[check_depth] {kk} : No string")
                        else:
                            self.logger.error(f"method is not prepared")
                            return 0 
                                                
                        dicts[f"element_{kk}_{depth_level}"]=str
                list_items_decoding.append(dicts)
            results=pd.DataFrame(list_items_decoding)
        else:
            df=pd.DataFrame()
            for i in list_items:

                strs=""
                str=i.get_attribute('innerHTML')
                cleaned_str=re.sub(r'<[/a-z,A-Z]+>',"",str)
                strs=f"{strs} {cleaned_str}"
                n+=1
    
                if type(card)!=dict:
                    ret=pd.Series({
                        f"order_{depth_level}" : n,
                        f"element_title_{depth_level}" : i.get_attribute('title'),
                        f"element_name_{depth_level}" : cleaned_str,
                        f"element_href_{depth_level}"  : i.get_attribute('href'),
                        f"element_class_{depth_level}" : i.get_attribute('class'),
                    })
                else:
                    dicts=dict()
                    for kk in card.keys():
                        case=card[kk].split("_")
                        if case[0]=="tag":
                            try: 
                                self.logger.debug(f"[check_depth] : {case[0]}")
                                str=i.find_element(By.TAG_NAME,case[1]).get_attribute(case[-1])
                            except:
                                str=None
                                self.logger.info(f"[check_depth] {kk} : No string")
                        elif case[0]=="class":
                            try: 
                                self.logger.debug(f"[check_depth] : {case[0]}")
                                str=i.find_element(By.CLASS_NAME,case[1]).get_attribute(case[-1])
                            except:
                                str=None
                                self.logger.info(f"[check_depth] {kk} : No string")
                        elif case[0]=="XPATH":
                            try:
                                self.logger.debug(f"[check_depth] : {case[0]}")
                                str=i.find_element(By.XPATH,case[1]).get_attribute(case[-1])
                            except:
                                str=None
                                self.logger.info(f"[check_depth] {kk} : No string")
                        else:
                            self.logger.error(f"method is not prepared")
                            return 0               
                        dicts[f"element_{kk}_{depth_level}"]=str
                    ret=pd.Series(dicts)
                ret=pd.concat([before_info,ret],axis=0)
                rets=pd.DataFrame(ret).T
                df=pd.concat([df,rets],axis=0,ignore_index=False)
            results=df
        self.logger.info(f"Strings : {str}")
        self.logger.info(f"number of target : {n}")
        return list_items, results        
    def activate_depth(self,depth_list:list,checker,depth_level:int=None,before_info:pd.DataFrame=None):
        '''
        activate with depth checker
        dependency : check_depth       
        '''
        assert ~((type(depth_level) != None)^(type(before_info) != None)), "depth level & before info should be provided together"

        results=pd.DataFrame()
        if depth_level == None:
            '''
            TODO
            '''
            self.logger.info("[activate_depth]before_depth : None")
        else:
            for i,info in zip(depth_list,before_info.iloc):
                i.click()
                WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,checker)))
                self.logger.info(f"[activate_depth] depth: health check done")
                self.logger.info(f"[activate_depth] getter: single level get :[{info.iloc[1]}]")
                list_items,checked_depth_results=self.check_depth(checker,depth_level=depth_level,before_info=info)
                self.logger.info(f"[activate_depth] getter: single info get done")
                results=pd.concat([results,checked_depth_results],axis=0,ignore_index=False)
                # except: 
                #     self.logger.error(f"[activate_depth] depth: health check error.")

            return list_items, results
    def activate_href_with_card(
        self,
        checker:str,
        sub_checker:str,
        depth_level:int=None,
        before_info:pd.DataFrame=None,
        card:dict=None
        )-> pd.DataFrame():
        '''
        activate with depth checker
        dependency : check_depth       
        '''
        assert ~((type(depth_level) != None)^(type(before_info) != None)), "depth level & before info should be provided together"

        results=pd.DataFrame()
        if depth_level == None:
            '''
            TODO
            '''
            self.logger.info("[activate_depth] before_depth : None")
            self.logger.error("depth_level should be provided")
            return 0
        else:
            target_col=f"element_href_{depth_level-1}"
            assert target_col in before_info, "href target is not existed, [depthLv:{depth_level}]"
            for info in before_info.iloc:
                self.driver.get(info[target_col])
                try:
                    WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,checker)))
                except:
                    self.logger.warning("[activate_herf] 400 error")
                    WebDriverWait(self.driver,10)
                    self.driver.delete_all_cookies()
                    self.driver.get(info[target_col])
                    WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,sub_checker)))
                self.logger.info(f"[activate_herf] depth: health check done")
                self.logger.info(f"[activate_herf] getter: single level get :[{info.iloc[1]}]")
                if type(card)==dict:
                    list_items,checked_depth_results=self.check_depth(checker,depth_level=depth_level,before_info=info,card=card)
                else:
                    list_items,checked_depth_results=self.check_depth(checker,depth_level=depth_level,before_info=info)
                self.logger.info(f"[activate_depth] getter: single info get done")
                results=pd.concat([results,checked_depth_results],axis=0,ignore_index=False)
                # except: 
                #     self.logger.error(f"[activate_depth] depth: health check error.")
            results=results.reset_index()
            return list_items, results    
    def activate_single_depth_info(
            self,
            before_info_series:pd.Series,
            depth_level:int=None,
            custom_checker=None,
            custom_getter=None,
        )-> pd.Series():
        '''
        TODO writing help
        '''
        information=None

        if depth_level is None:
            self.logger.info("[add_single_depth_info] depth_level : None")
            self.logger.error("depth_level should be provided")
            return 0
        else:
            self.logger.info(f"[add_single_depth_info] depth_level : {depth_level}")
            self.driver.get(before_info_series[f"element_href_{depth_level}"])

        ## custom checker

        if type(custom_checker)!=None:
            self.logger.info(f"[add_single_depth_info] custom_checker : called")
            custom_checker(class_object=self)
            self.logger.info(f"[add_single_depth_info] custom_checker : done")
        
        if type(custom_getter)!=None:
            self.logger.info(f"[add_single_depth_info] custom_getter : called")
            information=custom_getter(class_object=self)
            self.logger.info(f"[add_single_depth_info] custom_getter : done")
            before_info_series[f"element_custom_info_{depth_level}"]=information

        results=before_info_series
        return results

    
    '''
    main scripts
    - top down
    - bottom up
    '''

    def run_scripts_top_down(self):
        self.logger.info("start run_script")
        '''
        

        '''
        _path=os.path.join(os.getcwd(),'local_crawler','script','case_1.json')


        with open(_path,"r") as f:
            scripts=json.load(f)
        ### TODO ACTION coding
        
        max_action=scripts["max_action"]
        target=scripts["target"]
        landing_check=scripts["landing_page_checker"]
        target_check=scripts["target_checker"]
        sub_check=scripts["sub_checker"]
        target_card=scripts["cards"]

        self.logger.info(f"making chrome concole : {target}")
        self.driver.get(target) 
        self.check_loading(landing_check)
        
        ele,df=self.check_depth(
            checker=target_check[0]
            )
        
        _,df=self.activate_depth(
            depth_list=ele,
            checker=target_check[1],
            depth_level=2,
            before_info=df
            )

        _,df=self.activate_href_with_card(
            checker=target_check[2],
            sub_checker=sub_check,
            depth_level=3,
            before_info=df,
            card=target_card
            )
        
        self.logger.info("single level search")

        return df

    def run_scripts_bottom_up(self,df:pd.DataFrame=None):
        self.logger.info("start run_script")
        self.logger.info("single_items")
        ### bottom sheet check
        
        _path=os.path.join(os.getcwd(),'local_crawler','script','case_2_unstructed.json')
        with open(_path, "r") as f:
            case_2_info=json.load(f)

        if df is None:
            df=pd.DataFrame({"element_href_3":[case_2_info["href_sample"]]})

        from script.custom_script import custom_checker,custom_getter

        for df_series in df.iloc:
            df_series=self.activate_single_depth_info(
                depth_level=3,
                before_info_series=df_series,
                custom_checker=custom_checker,
                custom_getter=custom_getter
            )

            _,df=self.check_depth(
                checker=case_2_info["checker"],
                depth_level=4,
                before_info=df_series,
                card=case_2_info["cards"],
            )
            
            ## 구조 확인
            ## 파일 수집



            ## //*[@id="2"]/div/span/img


            self.logger.info("single item done")

        

        

        
        
        







        
        
    
if __name__=="__main__":
    '''
    크롤러의 기본 설정은 단위함수들의 pytest 용도로 사용 예정
    '''
            
    #### logging
   
    c=cbase(headless=True)

    results=c.run_scripts_bottom_up()

    print("done")


    #### pytest
    ### Target_1. 공공 데이터 크롤링
    ### 데이터를 
    
    
    

    
    
    















