from example.commons import Faker
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
from pyecharts.charts import Map
def map_hangzhou() -> Map:
    c = (
        Map()
        .add("商家A", [list(z) for z in zip(['余杭区','西湖区','滨江区','下沙区','上城区'], Faker.values())], "杭州")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-杭州地图"),
            visualmap_opts=opts.VisualMapOpts(),
        )
    )
    return c
map_hangzhou().render('gd.html')


