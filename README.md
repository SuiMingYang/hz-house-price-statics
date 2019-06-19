# 杭州房价分析

### 一、项目主题
分析杭州历年城区内小区房价变化，根据房地产知识定义楼盘，为用户购房提供决策参考。

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

树形结构嵌套请求，可以用for循环，可以用队列。

执行crawl_data.py脚本

##### 2.数据预处理
清洗脏数据，整理数据维度。
###### （1）缺省值处理
缺少的值不容易估算，删除。

###### （2）数据归一化

###### （3）

执行data_analysis.py脚本

##### 3.数据分析
###### （1）建立指标体系
房地产指标，定义楼盘，分类。
环比，同比-增长，下跌

###### （2）楼盘关联指标

###### （3）数据可视化

##### 4.数据预测
###### （1）模型选择
微观层面上可以预测，但是实际上会受政策，经济等因素的影响，所以预测仅仅是在微观层面上，即仅考虑指标和数值的维度上，提供参考
###### （2）参数调优

###### （3）输出分类结果



-----

### 三、项目结论
##### 1.
###### （1）

##### 2.
###### （1）


----

Author: suimingyang 

Email : suimingyang123@gmail.com

Blog  : [https://suimingyang.github.io/](https://suimingyang.github.io/)

----



