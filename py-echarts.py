'''
from example.commons import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Page, Pie, Timeline


def timeline_bar() -> Timeline:
    x = Faker.choose()
    tl = Timeline()
    for i in range(2015, 2020):
        bar = Bar()
            
        bar.add_xaxis(x)
        for j,item in enumerate(x):
            bar.add_yaxis(x[j], [Faker.values()[j]])
        bar.set_global_opts(title_opts=opts.TitleOpts("某商店{}年营业额".format(i)))
    
        tl.add(bar, "{}年".format(i))
    return tl
timeline_bar().render()
'''
from example.commons import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line,Scatter,Timeline,Page, Pie
import pandas as pd
import numpy as np

data=pd.read_csv('./data_history/houseprice.csv')
time_list=data.groupby(['dates'])
data_group=data.groupby(['name'])
print(len(data_group))
name_list=[]
time_range=[]
for i,name in enumerate(data_group):
    if i<10:
        name_list.append(name[0])

for i,name in enumerate(time_list):
    if i<10:
        time_range.append(name[0])

chart_count=2
legend_count=5
name_list=np.array(name_list).reshape(chart_count,legend_count)

def grid_vertical() -> Grid:
    #grid=Grid()
    #for item in name_list:
    tl=Timeline()
    for t in time_range:
        bar=Bar()
        bar.add_xaxis(name_list[0])
        for name in name_list[0]:
            price_list=list(data[(data['name']==name) & (data['dates']== t) ]['price'])
            if len(price_list)==0:
                bar.add_yaxis(name, [0],category_gap='5%',gap='5%')
            else:
                bar.add_yaxis(name, price_list,category_gap='5%',gap='5%')
        bar.set_global_opts(title_opts=opts.TitleOpts("某商店{}营业额".format(t)))
        tl.add(bar, "{}年".format(t))
        #grid.add(tl, grid_opts=opts.GridOpts(pos_bottom="60%"))
        tl.add_schema(is_auto_play=True,play_interval=1000)
    return tl#grid

grid_vertical().render()

# from example.commons import Faker
# from pyecharts import options as opts
# from pyecharts.charts import Bar, Grid, Line,Scatter

# from pyecharts.charts import Bar, Page, Pie, Timeline


# def timeline_bar() -> Timeline:
#     x = Faker.choose()
#     tl = Timeline()
#     for i in range(2015, 2020):
#         bar = (
#             Bar()
#             .add_xaxis(x)
#             .add_yaxis("商家A", Faker.values())
#             .add_yaxis("商家B", Faker.values())
#             .set_global_opts(title_opts=opts.TitleOpts("某商店{}年营业额".format(i)))
#         )
#         tl.add(bar, "{}年".format(i))
#     return tl

# def grid_vertical() -> Grid:
#     bar = (
#         Bar()
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .set_global_opts(title_opts=opts.TitleOpts(title="Grid-Bar"))
#     )
#     grid = (
#         Grid()
#         .add(bar, grid_opts=opts.GridOpts(pos_bottom="40%"))
#         .add(bar, grid_opts=opts.GridOpts(pos_top="40%"))
#     )
#     return grid

# grid_vertical().render()