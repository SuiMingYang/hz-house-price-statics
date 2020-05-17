import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

data = pd.read_csv('./data_history/houseprice.csv')

data=data.groupby(['name'])
row=len(data)
sub=row
plt.figure(figsize=(50,40))
plt.tight_layout()#调整整体空白

# 找出趋势上升的楼盘

for i,item in enumerate(data):
    if i>9:
        break

    plt.subplot(10,5,i+1)
    plt.plot(range(len(item[1]['dates'])),item[1]['price'],label=item[0])
    #plt.subplots_adjust(left=0.7,bottom=0.1, right=0.8, top=0.2)
    plt.subplots_adjust(wspace =0.5, hspace =0.5)#调整子图间距
    plt.legend(loc='upper left')

plt.suptitle(u'杭州房价变化图')
plt.savefig('fangjia.jpg',bbox_inches='tight')
plt.show()



