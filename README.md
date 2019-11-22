# 杭州房源分析

### 一、项目主题
分析杭州历年城区内小区房价变化，根据房地产知识定义楼盘，为用户购房提供决策参考。（可分析其他城市，替换第一个城区链接即可。）

房源网站数据全，但是量过大，我们只针对小区这一维度，给出纵向和横向对比的维度数据，做内容聚合。

----

### 二、项目开发

##### 1.数据爬虫
获取房天下的数据源，数据入库。

指标：小区名，房价，经度，纬度，板块评级，物业评级，活跃度评级，教育评级，搜索热度。

待分析出的指标：同比，环比，分类，综合评分，预测房价。
###### （1）分析网站结构

主城区链接：get请求
    https://fangjia.fang.com/fangjia/map/getmapdata/hz?district=&commerce=&x1=undefined&y1=undefined&x2=undefined&y2=undefined&v=20150116&newcode=

商业区：get请求
    https://fangjia.fang.com/fangjia/map/getmapdata/hz?district=%E6%8B%B1%E5%A2%85&commerce=&x1=undefined&y1=undefined&x2=undefined&y2=undefined&v=20150116&newcode=

小区：get请求
    https://fangjia.fang.com/fangjia/map/getmapdata/hz?district=%E6%8B%B1%E5%A2%85&commerce=&x1=undefined&y1=undefined&x2=undefined&y2=undefined&v=20150116&newcode=

历年：get请求
    https://fangjia.fang.com/fangjia/common/ajaxdetailtrenddata/hz?dataType=proj&projcode=2010780380&year=2

requests请求数据接口，selenium获取页面静态数据。

selenium有点慢，5小时可爬到杭州小区全部数据。中间会有反爬机制，弹出验证码页面，导致查不到页面元素，可以监听异常，手动输入验证码，或者用图像识别自动输入，我嫌麻烦就手动了，大概输入个5、6次，后期核心业务做好了，再加图像识别这块。

树形结构嵌套请求，可以用for循环，可以用队列。

执行`crawl_data.py`脚本，看着数据一条一条的录入，小有成就感。

##### 2.数据预处理
清洗脏数据，整理数据维度。
这个过程可以说是最麻烦的了，各种不确定，不规范的数据，都要在这阶段解决，处理成规范的可用的数据。

###### （1）缺省值处理
缺少的值不容易估算，先填充0，不影响计算，后面为了表现缺省值再填充-1。

###### （2）数据归一化
`活跃度评级`、`板块评级`、`物业评级`、`教育评级`取值区间[**A,B,C,D**]
`搜索指数`取值区间 **0-50**
假设这些指标在一个量化维度，令**A=10，B=7.5，C=5，D=2.5，default=0，搜索指数/5**，归一化到**0-10**，五个值之和可以看做一个简单维度的评分。

<font color="#dd0000">待开发：后面四个大文本字段信息量太大，需要正则抽取指标，后期再细化建模。</font><br/> 


###### （3）

执行`data_analysis.py`脚本

##### 3.数据分析
###### （1）建立指标体系
房地产指标，定义楼盘，分类。
环比，同比-增长，下跌

###### （2）楼盘关联指标
选筹，
返租，
远大大（远郊，大盘，大户型），
公寓，
商铺，
标杆盘，
别墅，

中央商务区，
地铁投资，
被城市包住的郊区
睡城
城乡结合部
新区
学区房
笋盘


###### （3）数据可视化
地图展示：百度地图，echarts
可视化找了几个工具，arcgis for python的mapview对象不好用，且只支持jupyter的展示，geopandas没有具象到街道和小区，还是百度地图最香，统计图表用echarts。

##### 4.数据预测
###### （1）模型选择
微观层面上可以预测，但是实际上会受政策，经济等因素的影响，所以预测仅仅是在微观层面上，即仅考虑指标和数值的维度上，提供参考。
###### （2）参数调优

###### （3）输出分类结果

###### （4）房源评估系统


-----

### 三、项目结论
##### 1.
###### （1）

##### 2.
###### （1）

[源码地址](https://github.com/SuiMingYang/hz-house-price-statics)
----

Author: suimingyang 

Email : suimingyang123@gmail.com

Blog  : [https://suimingyang.github.io/](https://suimingyang.github.io/)

----
