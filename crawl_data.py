import requests
import pandas as pd
import numpy as np
import time
from pandas.tseries.offsets import Day
from urllib import parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import time
import random

class Driver(object):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
        # 加代理ip池
        # chrome_options.add_argument("--proxy-server=http://222.240.184.126:8086")
        chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败

        self.driver = webdriver.Chrome(options=chrome_options)

class Load_Data(object):
    def __init__(self):

        # 地区：树结构
        self.area_tree={
            "area_name":[],
            "area_parent":[],
            "area_price":[],
            "area_x_value":[],
            "area_y_value":[],
            "area_url_val":[],
            "area_stage":[]
        }

        # 小区详细数据
        self.estate_obj={
            'estate_name':[], #小区名
            'estate_house_resources':[], #房源数
            'estate_sales_count':[], #销量
            'estate_activity_rate':[], #活跃度评级
            'estate_property_rate':[], #物业评级
            'estate_education_rate':[], #教育评级
            'estate_plate_rate':[], #板块评级
            'estate_search_rate':[], #搜索热度

            'estate_basic_info':[], #基础信息
            'estate_amenities_info':[], #配套设施信息
            'estate_traffic_info':[], #交通信息信息
            "estate_around_instrument_info":[] #周边设施信息
        }

        # 月度房价数据
        self.detail_obj={
            'detail_estate':[], #小区名
            'detail_date':[], #日期
            'detail_price':[] #价格
        }
    
    def get_block_list(self):
        block_url='https://fangjia.fang.com/fangjia/map/getmapdata/hz?district=&commerce=&x1=undefined&y1=undefined&x2=undefined&y2=undefined&v=20150116&newcode='
        block_res=self.get_req(block_url)
        self.block_list=block_res.json()['project']
        print("杭州市区数：",len(self.block_list))
        return self.block_list

    def load_block(self,block,driver):
        self.area_tree["area_name"].append(block["name"])
        self.area_tree["area_price"].append(block["price"])
        self.area_tree["area_x_value"].append(block["px"])
        self.area_tree["area_y_value"].append(block["py"])
        self.area_tree["area_url_val"].append(block["url"])
        self.area_tree["area_parent"].append('杭州')
        self.area_tree["area_stage"].append(1)
        
        estate_url='https://fangjia.fang.com/fangjia/map/getmapdata/hz?district=%s&commerce=&x1=undefined&y1=undefined&x2=undefined&y2=undefined&v=20150116&newcode=' % parse.quote(block['name'])
        estate_res=self.get_req(estate_url)
        estate_list=estate_res.json()
        
        print(block["name"],"区有",len(estate_list['project']),"个片区")
        for estate in estate_list['project']:
            self.load_estate(estate,block,driver)

    def load_estate(self,estate,block,driver):
        self.area_tree["area_name"].append(estate["name"])
        self.area_tree['area_price'].append(estate["price"])
        self.area_tree['area_x_value'].append(estate["px"])
        self.area_tree['area_y_value'].append(estate["py"])
        self.area_tree['area_url_val'].append(estate["url"])
        self.area_tree['area_parent'].append(block["name"])
        self.area_tree['area_stage'].append(2)

        valiage_url='https://fangjia.fang.com/fangjia/map/getmapdata/hz?district=%s&commerce=%s&x1=%s&y1=%s&x2=%s&y2=%s&v=20150116&newcode=' % (parse.quote(block['name']),parse.quote(estate['name']),block['px'],block['py'],estate['px'],estate['py'])
        valiage_res=self.get_req(valiage_url)
        valiage_list=valiage_res.json()
        
        print(estate["name"],"片区有",len(valiage_list['project']),"个小区")
        for valiage in valiage_list['project']:
            self.load_valiage(valiage,estate,block,driver)

    def load_valiage(self,valiage,estate,block,driver):
        self.area_tree['area_name'].append(valiage["name"])
        self.area_tree['area_price'].append(valiage["price"])
        self.area_tree['area_x_value'].append(valiage["px"])
        self.area_tree['area_y_value'].append(valiage["py"])
        self.area_tree['area_url_val'].append(valiage["url"])
        self.area_tree['area_parent'].append(estate["name"])
        self.area_tree['area_stage'].append(3)

        self.estate_obj['estate_name'].append(valiage["name"])
        print(valiage["name"])
        url_res=self.get_page_url(valiage,driver)
        if url_res:
            pass
        else:
            # 验证码异常处理
            self.load_valiage(valiage,estate,block,driver)
            return False
        star_res,estate_param = self.get_page_star(driver)
        detail_res=self.get_detail_info(estate_param,valiage,estate,driver)
        #self.get_grade_data()
        self.get_history_price(valiage)

    def get_page_url(self,valiage,driver):
        try:
            #获取页面静态数据
            driver.get("http:%s" % valiage["url"]) 
            #self.estate_obj['estate_search_rate'].append(driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div[3]/ul/li[1]/b').text)
            self.estate_obj['estate_search_rate'].append(' ')
            return True
        except Exception as e:
            print("获取小区路径报错：",e)
            if driver.current_url.find('code')>-1:
                #driver.find_element_by_xpath('//*[@id="verify_page"]/div/div[2]/p').text=="请输入图片中的验证码：":
                # 重新导入这条
                return False
            else:
                self.estate_obj['estate_search_rate'].append(" ")
                return True

    def get_page_star(self,driver):
        try:
            estate_param=driver.find_element_by_xpath('//*[@id="pcxqfangjia_B02_01"]').get_attribute('href') 
            driver.get(estate_param)
            
            js = "document.getElementById('main').children[1].style.display='block'"
            driver.execute_script(js)

            # 点击，获取静态页面
            self.estate_obj['estate_house_resources'].append(driver.find_element_by_xpath('//*[@id="xqwxqy_C01_16"]/a[1]/div/p[2]').text)
            self.estate_obj['estate_sales_count'].append(driver.find_element_by_xpath('//*[@id="xqwxqy_C01_16"]/a[2]/div/p[2]').text)
            tag=driver.find_element_by_xpath('//*[@id="main"]/div[2]')
            try:
                driver.find_element_by_xpath('//*[@id="main"]/div[1]').click()
            except Exception as e:
                print("点击隐藏标签报错：",e)
            
            self.estate_obj['estate_activity_rate'].append(tag.text.split('\n')[1].split(':')[1].replace(' ','')) #活跃度评级
            self.estate_obj['estate_property_rate'].append(tag.text.split('\n')[2].split(':')[1].replace(' ','')) #物业评级
            self.estate_obj['estate_education_rate'].append(tag.text.split('\n')[3].split(':')[1].replace(' ','')) #教育评级
            self.estate_obj['estate_plate_rate'].append(tag.text.split('\n')[4].split(':')[1].replace(' ','')) #板块评级

            #===================请求次数多进入验证码模式=====================#
            #===================图像识别=====================#
            #===================或者打断点手动输入=====================#

            #===================验证码输入几次之后会失去作用，无法请求页面=====================#
            return True,estate_param
        except Exception as e:
            print("获取小区评星报错：",e)
            if driver.current_url.find('code')>-1:
                #driver.find_element_by_xpath('//*[@id="verify_page"]/div/div[2]/p').text=="请输入图片中的验证码：":
                # 重新导入这条
                return False,''
            else:
                self.estate_obj['estate_house_resources'].append(" ")
                self.estate_obj['estate_sales_count'].append(" ")
                self.estate_obj['estate_activity_rate'].append(" ")
                self.estate_obj['estate_property_rate'].append(" ")
                self.estate_obj['estate_education_rate'].append(" ")
                self.estate_obj['estate_plate_rate'].append(" ")
                return True,estate_param

    def get_detail_info(self,estate_param,valiage,estate,driver):
        try:
            #维度，全部信息，待清洗
            driver.get(estate_param+"/xiangqing/")
            
            basic_info=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[2]/div[2]/dl').text
            amenities_info=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[3]/div[2]/dl').text
            traffic_info=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[4]/div[2]/dl').text
            around_instrument=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[5]/div[2]/dl').text
            
            self.estate_obj['estate_basic_info'].append(basic_info)
            self.estate_obj['estate_amenities_info'].append(amenities_info)
            self.estate_obj['estate_traffic_info'].append(traffic_info)
            self.estate_obj['estate_around_instrument_info'].append(around_instrument)
            return True
        except Exception as e:
            print("获取小区信息报错：",e)
            if driver.current_url.find('code')>-1:
                #driver.find_element_by_xpath('//*[@id="verify_page"]/div/div[2]/p').text=="请输入图片中的验证码：":
                # 重新导入这条
                #self.load_valiage(valiage,estate,block)
                return False
            else:
                self.estate_obj['estate_basic_info'].append(" ")
                self.estate_obj['estate_amenities_info'].append(" ")
                self.estate_obj['estate_traffic_info'].append(" ")
                self.estate_obj['estate_around_instrument_info'].append(" ")
                return True
            '''
    
    def get_grade_data(self):
        try:
            # 评级数据完善
            driver.get(estate_param+"/pingji/")
            
            basic_info=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[2]/div[2]/dl').text
            amenities_info=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[3]/div[2]/dl').text
            traffic_info=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[4]/div[2]/dl').text
            around_instrument=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[5]/div[2]/dl').text
            
            self.estate_obj['estate_basic_info'].append(basic_info)
            self.estate_obj['estate_amenities_info'].append(amenities_info)
            self.estate_obj['estate_traffic_info'].append(traffic_info)
            self.estate_obj['estate_around_instrument_info'].append(around_instrument)
        except Exception as e:
            print("获取小区评级报错：",e)
            '''
    
    def get_history_price(self,valiage):
        detail_url='https://fangjia.fang.com/fangjia/common/ajaxdetailtrenddata/hz?dataType=proj&projcode=%s&year=2' % valiage["url"].split('/')[-1].split('.')[0]
        detail_res=self.get_req(detail_url)
        detail_list=detail_res.json() #两年的详细数据
        for detail in detail_list:
            #print(valiage["name"],"小区数据",len(detail_list))
            self.detail_obj['detail_estate'].append(valiage["name"])
            self.detail_obj['detail_price'].append(detail[1])
            timeArray = time.localtime(detail[0]/1000)
            otherStyleTime = time.strftime("%Y-%m", timeArray)
            self.detail_obj['detail_date'].append(otherStyleTime)

    def data2csv(self):
        geography_data = {
            "name":pd.Series(self.area_tree['area_name']),
            "parent":pd.Series(self.area_tree['area_parent']),
            "price": pd.Series(self.area_tree['area_price']),
            "longitude":pd.Series(self.area_tree['area_x_value']),
            "latitude": pd.Series(self.area_tree['area_y_value']),
            "url":pd.Series(self.area_tree['area_url_val']),
            "area_stage":pd.Series(self.area_tree['area_stage'])
        }
        geography_df = pd.DataFrame(geography_data,index=None)
        geography_df.to_csv('./data/geography_tree.csv',index=False)


        horse_info_data = {
            "name":pd.Series(self.estate_obj['estate_name']),
            "house_resources":pd.Series(self.estate_obj['estate_house_resources']),
            "sales_count":pd.Series(self.estate_obj['estate_sales_count']),
            "activity_rate":pd.Series(self.estate_obj['estate_activity_rate']),
            "property_rate":pd.Series(self.estate_obj['estate_property_rate']),
            "education_rate":pd.Series(self.estate_obj['estate_education_rate']),
            "plate_rate":pd.Series(self.estate_obj['estate_plate_rate']),
            "search_rate":pd.Series(self.estate_obj['estate_search_rate']),
            "basic_info":pd.Series(self.estate_obj['estate_basic_info']),
            "amenities_info":pd.Series(self.estate_obj['estate_amenities_info']),
            "traffic_info":pd.Series(self.estate_obj['estate_traffic_info']),
            "around_instrument_info":pd.Series(self.estate_obj['estate_around_instrument_info'])
        }
        houseinfo_df = pd.DataFrame(horse_info_data,index=None)
        houseinfo_df.to_csv('./data/houseinfo.csv',encoding="utf-8",index=False)


        houseprice_data = {
            "name":pd.Series(self.detail_obj['detail_estate']),
            #'type':pd.Series(np.full([1,len(estate_name)],' ')[0]),
            "price": pd.Series(self.detail_obj['detail_price']),
            "date":pd.Series(self.detail_obj['detail_date']),
        }
        houseprice_df = pd.DataFrame(houseprice_data,index=None)
        houseprice_df.to_csv('./data/houseprice.csv',encoding="utf-8")

    def get_req(self,url):
        pro = ['222.240.184.126:8086', '210.26.64.44:3128', '121.69.46.177:9000'] 
        proxy={'http': random.choice(pro)}
        USER_AGENTS = [
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
        ]
 
        user_agent = random.choice(USER_AGENTS)
        return requests.get(url,proxies=proxy,headers={'User-Agent':user_agent})

if __name__ == "__main__":
    load_data=Load_Data()
    block_list=load_data.get_block_list()
    dri=[]
    
    for i in range(4):
        dri.append(Driver().driver)
        #load_data.load_block(block,dri)
    
    executor=ThreadPoolExecutor(max_workers=4)
    result=executor.map(load_data.load_block,block_list,dri)

    for d in dri:
        d.quit()
    
'''
for block in block_list['project']:
#def request_block(block):
    #print("区：",block["name"],"有",len(block_list['project']),"个片区")
    self.area_tree["area_name"].append(block["name"])
    self.area_tree["area_price"].append(block["price"])
    self.area_tree["area_x_value"].append(block["px"])
    self.area_tree["area_y_value"].append(block["py"])
    self.area_tree["area_url_val"].append(block["url"])
    self.area_tree["area_parent"].append('杭州')
    self.area_tree["area_stage"].append(1)
    
    estate_url='https://fangjia.fang.com/fangjia/map/getmapdata/hz?district=%s&commerce=&x1=undefined&y1=undefined&x2=undefined&y2=undefined&v=20150116&newcode=' % parse.quote(block['name'])
    estate_res=self.get_req(estate_url)
    estate_list=estate_res.json()
    
    print(block["name"],"区有",len(estate_list['project']),"个片区")
    for estate in estate_list['project']:
        self.area_tree["area_name"].append(estate["name"])
        self.area_tree['area_price'].append(estate["price"])
        self.area_tree['area_x_value'].append(estate["px"])
        self.area_tree['area_y_value'].append(estate["py"])
        self.area_tree['area_url_val'].append(estate["url"])
        self.area_tree['area_parent'].append(block["name"])
        self.area_tree['area_stage'].append(2)

        valiage_url='https://fangjia.fang.com/fangjia/map/getmapdata/hz?district=%s&commerce=%s&x1=%s&y1=%s&x2=%s&y2=%s&v=20150116&newcode=' % (parse.quote(block['name']),parse.quote(estate['name']),block['px'],block['py'],estate['px'],estate['py'])
        valiage_res=self.get_req(valiage_url)
        valiage_list=valiage_res.json()
        
        print(estate["name"],"片区有",len(valiage_list['project']),"个小区")
        for valiage in valiage_list['project']:
            self.area_tree['area_name'].append(valiage["name"])
            self.area_tree['area_price'].append(valiage["price"])
            self.area_tree['area_x_value'].append(valiage["px"])
            self.area_tree['area_y_value'].append(valiage["py"])
            self.area_tree['area_url_val'].append(valiage["url"])
            self.area_tree['area_parent'].append(estate["name"])
            self.area_tree['area_stage'].append(3)

            self.estate_obj['estate_name'].append(valiage["name"])
            print(valiage["name"])
            
            try:
                #获取页面静态数据
                driver.get("http:%s" % valiage["url"]) 
                self.estate_obj['estate_search_rate'].append(driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div[3]/ul/li[1]/b').text)
                
                estate_param=driver.find_element_by_xpath('//*[@id="pcxqfangjia_B02_01"]').get_attribute('href') 
                driver.get(estate_param)
                
                js = "document.getElementById('main').children[1].style.display='block'"
                driver.execute_script(js)

                # 点击，获取静态页面
                self.estate_obj['estate_house_resources'].append(driver.find_element_by_xpath('//*[@id="xqwxqy_C01_16"]/a[1]/div/p[2]').text)
                self.estate_obj['estate_sales_count'].append(driver.find_element_by_xpath('//*[@id="xqwxqy_C01_16"]/a[2]/div/p[2]').text)
                tag=driver.find_element_by_xpath('//*[@id="main"]/div[2]')
                try:
                    driver.find_element_by_xpath('//*[@id="main"]/div[1]').click()
                except Exception as e:
                    print("点击隐藏标签报错：",e)

                self.estate_obj['estate_activity_rate'].append(tag.text.split('\n')[1].split(':')[1].replace(' ','')) #活跃度评级
                self.estate_obj['estate_property_rate'].append(tag.text.split('\n')[2].split(':')[1].replace(' ','')) #物业评级
                self.estate_obj['estate_education_rate'].append(tag.text.split('\n')[3].split(':')[1].replace(' ','')) #教育评级
                self.estate_obj['estate_plate_rate'].append(tag.text.split('\n')[4].split(':')[1].replace(' ','')) #板块评级
                
                
                #===================请求次数多进入验证码模式=====================#
                #===================图像识别=====================#
                #===================或者打断点手动输入=====================#

                #===================验证码输入几次之后会失去作用，无法请求页面=====================#


                #维度，全部信息，待清洗
                driver.get(estate_param+"/xiangqing/")
                
                basic_info=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[2]/div[2]/dl').text
                amenities_info=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[3]/div[2]/dl').text
                traffic_info=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[4]/div[2]/dl').text
                around_instrument=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[5]/div[2]/dl').text
                
                self.estate_obj['estate_basic_info'].append(basic_info)
                self.estate_obj['estate_amenities_info'].append(amenities_info)
                self.estate_obj['estate_traffic_info'].append(traffic_info)
                self.estate_obj['estate_around_instrument_info'].append(around_instrument)
                
                # # 评级数据完善
                # driver.get(estate_param+"/pingji/")
                
                # basic_info=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[2]/div[2]/dl').text
                # amenities_info=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[3]/div[2]/dl').text
                # traffic_info=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[4]/div[2]/dl').text
                # around_instrument=driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[5]/div[2]/dl').text
                
                # self.estate_obj['estate_basic_info'].append(basic_info)
                # self.estate_obj['estate_amenities_info'].append(amenities_info)
                # self.estate_obj['estate_traffic_info'].append(traffic_info)
                # self.estate_obj['estate_around_instrument_info'].append(around_instrument)
                
            except Exception as e:
                print("获取小区信息报错：",e)
                if driver.find_element_by_xpath('//*[@id="verify_page"]/div/div[2]/p').text=="请输入图片中的验证码：":
                    pass
                else:
                    pass

                # 没有评级信息，不执行后面的数据了
                self.estate_obj['estate_house_resources'].append(" ")
                self.estate_obj['estate_search_rate'].append(" ")
                self.estate_obj['estate_sales_count'].append(" ")
                self.estate_obj['estate_activity_rate'].append(" ")
                self.estate_obj['estate_property_rate'].append(" ")
                self.estate_obj['estate_education_rate'].append(" ")
                self.estate_obj['estate_plate_rate'].append(" ")
                self.estate_obj['estate_basic_info'].append(" ")
                self.estate_obj['estate_amenities_info'].append(" ")
                self.estate_obj['estate_traffic_info'].append(" ")
                self.estate_obj['estate_around_instrument_info'].append(" ")
            

            detail_url='https://fangjia.fang.com/fangjia/common/ajaxdetailtrenddata/hz?dataType=proj&projcode=%s&year=2' % valiage["url"].split('/')[-1].split('.')[0]
            detail_res=self.get_req(detail_url)
            detail_list=detail_res.json() #两年的详细数据
            for detail in detail_list:
                #print(valiage["name"],"小区数据",len(detail_list))
                self.detail_obj['detail_estate'].append(valiage["name"])
                self.detail_obj['detail_price'].append(detail[1])
                timeArray = time.localtime(detail[0]/1000)
                otherStyleTime = time.strftime("%Y-%m", timeArray)
                self.detail_obj['detail_date'].append(otherStyleTime)
'''
'''
executor=ThreadPoolExecutor(max_workers=len(block_list))
result=executor.map(load_block,block_list)
'''











    
