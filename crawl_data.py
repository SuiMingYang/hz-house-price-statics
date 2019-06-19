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
block_name=[]
block_price=[]
block_x_value=[]
block_y_value=[]
block_url_val=[]
stage=[]

# 详细数据
estate_name = [] #小区名
date = [] #日期
price = [] #价格
house_resources = [] #房源数
sales_count = [] #销量
activity_rate = [] #活跃度评级
property_rate = [] #物业评级
education_rate = [] #教育评级
plate_rate = [] #板块评级
search_rate = [] #搜索热度

print("杭州市区数：",len(block_list['project']))

for block in block_list['project']:
    #print("区：",block["name"],"有",len(block_list['project']),"个片区")
    block_name.append(block["name"])
    block_price.append(block["price"])
    block_x_value.append(block["px"])
    block_y_value.append(block["py"])
    block_url_val.append(block["url"])
    stage.append(1)
    
    estate_url='https://fangjia.fang.com/fangjia/map/getmapdata/hz?district=%s&commerce=&x1=undefined&y1=undefined&x2=undefined&y2=undefined&v=20150116&newcode=' % parse.quote(block['name'])
    estate_res=requests.get(estate_url)
    estate_list=estate_res.json()
    
    print(block["name"],"区有",len(estate_list['project']),"个片区")
    for estate in estate_list['project']:
        block_name.append(estate["name"])
        block_price.append(estate["price"])
        block_x_value.append(estate["px"])
        block_y_value.append(estate["py"])
        block_url_val.append(estate["url"])
        stage.append(2)

        valiage_url='https://fangjia.fang.com/fangjia/map/getmapdata/hz?district=%s&commerce=%s&x1=%s&y1=%s&x2=%s&y2=%s&v=20150116&newcode=' % (parse.quote(block['name']),parse.quote(estate['name']),block['px'],block['py'],estate['px'],estate['py'])
        valiage_res=requests.get(valiage_url)
        valiage_list=valiage_res.json()
        
        print(estate["name"],"片区有",len(valiage_list['project']),"个小区")
        for valiage in valiage_list['project']:
            block_name.append(valiage["name"])
            block_price.append(valiage["price"])
            block_x_value.append(valiage["px"])
            block_y_value.append(valiage["py"])
            block_url_val.append(valiage["url"])
            stage.append(3)
            is_commend=True
            try:
                #获取页面静态数据
                driver.get("http:%s" % valiage["url"]) 
                search_rate.append(driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div[3]/ul/li[1]/b').text)
                
                estate_param=driver.find_element_by_xpath('//*[@id="pcxqfangjia_B04_01"]').get_attribute('href') 
                driver.get(estate_param)
                
                js = "document.getElementById('main').children[1].style.display='block'"
                driver.execute_script(js)
            except Exception as e:
                print("获取详细页面报错：",e)
                is_commend=False
                # 没有评级信息，不执行后面的数据了
            

            detail_url='https://fangjia.fang.com/fangjia/common/ajaxdetailtrenddata/hz?dataType=proj&projcode=%s&year=2' % valiage["url"].split('/')[-1].split('.')[0]
            detail_res=requests.get(detail_url)
            detail_list=detail_res.json() #两年的详细数据
            for detail in detail_list:
                #print(valiage["name"],"小区数据",len(detail_list))
                estate_name.append(valiage["name"])
                price.append(detail[1])
                timeArray = time.localtime(detail[0]/1000)
                otherStyleTime = time.strftime("%Y-%m", timeArray)
                date.append(otherStyleTime)

                if is_commend:
                    # 点击，获取静态页面
                    house_resources.append(driver.find_element_by_xpath('//*[@id="xqwxqy_C01_16"]/a[1]/div/p[2]').text)
                    sales_count.append(driver.find_element_by_xpath('//*[@id="xqwxqy_C01_16"]/a[2]/div/p[2]').text)
                    tag=driver.find_element_by_xpath('//*[@id="main"]/div[2]')
                    try:
                        driver.find_element_by_xpath('//*[@id="main"]/div[1]').click()
                    except Exception as e:
                        print("获取详细信息报错：",e)

                    activity_rate.append(tag.text.split('\n')[1].split(':')[1].replace(' ','')) #活跃度评级
                    property_rate.append(tag.text.split('\n')[2].split(':')[1].replace(' ','')) #物业评级
                    education_rate.append(tag.text.split('\n')[3].split(':')[1].replace(' ','')) #教育评级
                    plate_rate.append(tag.text.split('\n')[4].split(':')[1].replace(' ','')) #板块评级
                else:
                    house_resources.append(" ")
                    sales_count.append(" ")
                    activity_rate.append(" ")
                    property_rate.append(" ")
                    education_rate.append(" ")
                    plate_rate.append(" ")
                

geography_data = {
    "name":pd.Series(block_name),
    "price": pd.Series(block_price),
    "longitude":pd.Series(block_x_value),
    "latitude": pd.Series(block_y_value),
    "url":pd.Series(block_url_val),
    "stage":pd.Series(stage)
}
geography_df = pd.DataFrame(geography_data,index=None)
geography_df.to_csv('./data/geography_tree.csv',index=False)


houseprice_data = {
    "name":pd.Series(estate_name),
    #'type':pd.Series(np.full([1,len(estate_name)],' ')[0]),
    "price": pd.Series(price),
    "date":pd.Series(date),
    "house_resources":pd.Series(house_resources),
    "sales_count":pd.Series(sales_count),
    "activity_rate":pd.Series(activity_rate),
    "property_rate":pd.Series(property_rate),
    "education_rate":pd.Series(education_rate),
    "plate_rate":pd.Series(plate_rate),
    "search_rate":pd.Series(search_rate)
}


houseprice_df = pd.DataFrame(houseprice_data,index=None)
houseprice_df.to_csv('./data/houseprice.csv',encoding="utf-8")









    
