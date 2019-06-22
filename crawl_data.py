import requests
import pandas as pd
import numpy as np
import time
from pandas.tseries.offsets import Day
from urllib import parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败

driver = webdriver.Chrome(options=chrome_options)

block_url='https://fangjia.fang.com/fangjia/map/getmapdata/hz?district=&commerce=&x1=undefined&y1=undefined&x2=undefined&y2=undefined&v=20150116&newcode='
block_res=requests.get(block_url)
block_list=block_res.json()

# 地区：树结构
area_name=[]
area_parent=[]
area_price=[]
area_x_value=[]
area_y_value=[]
area_url_val=[]
area_stage=[]

# 小区详细数据
estate_name = [] #小区名
estate_house_resources = [] #房源数
estate_sales_count = [] #销量
estate_activity_rate = [] #活跃度评级
estate_property_rate = [] #物业评级
estate_education_rate = [] #教育评级
estate_plate_rate = [] #板块评级
estate_search_rate = [] #搜索热度

estate_basic_info = [] #基础信息
estate_amenities_info = [] #配套设施信息
estate_traffic_info = [] #交通信息信息
estate_around_instrument_info = [] #周边设施信息


# 月度房价数据
detail_estate = [] #小区名
detail_date = [] #日期
detail_price = [] #价格


print("杭州市区数：",len(block_list['project']))

for block in block_list['project']:
    #print("区：",block["name"],"有",len(block_list['project']),"个片区")
    area_name.append(block["name"])
    area_price.append(block["price"])
    area_x_value.append(block["px"])
    area_y_value.append(block["py"])
    area_url_val.append(block["url"])
    area_parent.append('杭州')
    area_stage.append(1)
    
    estate_url='https://fangjia.fang.com/fangjia/map/getmapdata/hz?district=%s&commerce=&x1=undefined&y1=undefined&x2=undefined&y2=undefined&v=20150116&newcode=' % parse.quote(block['name'])
    estate_res=requests.get(estate_url)
    estate_list=estate_res.json()
    
    print(block["name"],"区有",len(estate_list['project']),"个片区")
    for estate in estate_list['project']:
        area_name.append(estate["name"])
        area_price.append(estate["price"])
        area_x_value.append(estate["px"])
        area_y_value.append(estate["py"])
        area_url_val.append(estate["url"])
        area_parent.append(block["name"])
        area_stage.append(2)

        valiage_url='https://fangjia.fang.com/fangjia/map/getmapdata/hz?district=%s&commerce=%s&x1=%s&y1=%s&x2=%s&y2=%s&v=20150116&newcode=' % (parse.quote(block['name']),parse.quote(estate['name']),block['px'],block['py'],estate['px'],estate['py'])
        valiage_res=requests.get(valiage_url)
        valiage_list=valiage_res.json()
        
        print(estate["name"],"片区有",len(valiage_list['project']),"个小区")
        for valiage in valiage_list['project']:
            area_name.append(valiage["name"])
            area_price.append(valiage["price"])
            area_x_value.append(valiage["px"])
            area_y_value.append(valiage["py"])
            area_url_val.append(valiage["url"])
            area_parent.append(estate["name"])
            area_stage.append(3)

            estate_name.append(valiage["name"])
            print(valiage["name"])
            
            try:
                #获取页面静态数据
                driver.get("http:%s" % valiage["url"]) 
                estate_search_rate.append(driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div[3]/ul/li[1]/b').text)
                
                estate_param=driver.find_element_by_xpath('//*[@id="pcxqfangjia_B02_01"]').get_attribute('href') 
                driver.get(estate_param)
                
                js = "document.getElementById('main').children[1].style.display='block'"
                driver.execute_script(js)

                # 点击，获取静态页面
                estate_house_resources.append(driver.find_element_by_xpath('//*[@id="xqwxqy_C01_16"]/a[1]/div/p[2]').text)
                estate_sales_count.append(driver.find_element_by_xpath('//*[@id="xqwxqy_C01_16"]/a[2]/div/p[2]').text)
                tag=driver.find_element_by_xpath('//*[@id="main"]/div[2]')
                try:
                    driver.find_element_by_xpath('//*[@id="main"]/div[1]').click()
                except Exception as e:
                    print("点击隐藏标签报错：",e)

                estate_activity_rate.append(tag.text.split('\n')[1].split(':')[1].replace(' ','')) #活跃度评级
                estate_property_rate.append(tag.text.split('\n')[2].split(':')[1].replace(' ','')) #物业评级
                estate_education_rate.append(tag.text.split('\n')[3].split(':')[1].replace(' ','')) #教育评级
                estate_plate_rate.append(tag.text.split('\n')[4].split(':')[1].replace(' ','')) #板块评级
                
                
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
                
                estate_basic_info.append(basic_info)
                estate_amenities_info.append(amenities_info)
                estate_traffic_info.append(traffic_info)
                estate_around_instrument_info.append(around_instrument)

            except Exception as e:
                print("获取小区信息报错：",e)
                if driver.find_element_by_xpath('//*[@id="verify_page"]/div/div[2]/p').text=="请输入图片中的验证码：":
                    pass
                else:
                    pass

                # 没有评级信息，不执行后面的数据了
                estate_house_resources.append(" ")
                estate_search_rate.append(" ")
                estate_sales_count.append(" ")
                estate_activity_rate.append(" ")
                estate_property_rate.append(" ")
                estate_education_rate.append(" ")
                estate_plate_rate.append(" ")
                estate_basic_info.append(" ")
                estate_amenities_info.append(" ")
                estate_traffic_info.append(" ")
                estate_around_instrument_info.append(" ")
            

            detail_url='https://fangjia.fang.com/fangjia/common/ajaxdetailtrenddata/hz?dataType=proj&projcode=%s&year=2' % valiage["url"].split('/')[-1].split('.')[0]
            detail_res=requests.get(detail_url)
            detail_list=detail_res.json() #两年的详细数据
            for detail in detail_list:
                #print(valiage["name"],"小区数据",len(detail_list))
                detail_estate.append(valiage["name"])
                detail_price.append(detail[1])
                timeArray = time.localtime(detail[0]/1000)
                otherStyleTime = time.strftime("%Y-%m", timeArray)
                detail_date.append(otherStyleTime)
                

geography_data = {
    "name":pd.Series(area_name),
    "parent":pd.Series(area_parent),
    "price": pd.Series(area_price),
    "longitude":pd.Series(area_x_value),
    "latitude": pd.Series(area_y_value),
    "url":pd.Series(area_url_val),
    "area_stage":pd.Series(area_stage)
}
geography_df = pd.DataFrame(geography_data,index=None)
geography_df.to_csv('./data/geography_tree.csv',index=False)


horse_info_data = {
    "name":pd.Series(estate_name),
    "house_resources":pd.Series(estate_house_resources),
    "sales_count":pd.Series(estate_sales_count),
    "activity_rate":pd.Series(estate_activity_rate),
    "property_rate":pd.Series(estate_property_rate),
    "education_rate":pd.Series(estate_education_rate),
    "plate_rate":pd.Series(estate_plate_rate),
    "search_rate":pd.Series(estate_search_rate),
    "basic_info":pd.Series(estate_basic_info),
    "amenities_info":pd.Series(estate_amenities_info),
    "traffic_info":pd.Series(estate_traffic_info),
    "around_instrument_info":pd.Series(estate_around_instrument_info)
}
houseinfo_df = pd.DataFrame(horse_info_data,index=None)
houseinfo_df.to_csv('./data/houseinfo.csv',encoding="utf-8",index=False)


houseprice_data = {
    "name":pd.Series(detail_estate),
    #'type':pd.Series(np.full([1,len(estate_name)],' ')[0]),
    "price": pd.Series(detail_price),
    "date":pd.Series(detail_date),
}
houseprice_df = pd.DataFrame(houseprice_data,index=None)
houseprice_df.to_csv('./data/houseprice.csv',encoding="utf-8")









    
