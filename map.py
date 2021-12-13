import requests
import json
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import GeoType, RenderType

url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
data = json.loads(requests.get(url=url).json()['data'])
china = data['areaTree'][0]['children']

data1 = []
for i in range(len(china)):
    data1.append([china[i]['name'], china[i]['total']['confirm']])

china_total = u" 累计确诊:" + str(data['chinaTotal']['confirm']) + \
              u" 现存确诊:" + str(data['chinaTotal']['nowConfirm']) + \
              u" 疑似:" + str(data['chinaTotal']['suspect']) + \
              u" 死亡:" + str(data['chinaTotal']['dead']) + \
              u" 更新日期:" + str(data['lastUpdateTime'])

sum = 10000
geo = (
    Geo(init_opts=opts.InitOpts(width="1200px", height="600px", bg_color="#404a59", page_title="全国疫情实时报告",
                                renderer=RenderType.SVG, theme="white"))  # 设置绘图尺寸，背景色，页面标题，绘制类型
        .add_schema(maptype="china", itemstyle_opts=opts.ItemStyleOpts(color="rgb(49,60,72)",
                                                                       border_color="rgb(0,0,0)"))  # 中国地图，地图区域颜色，区域边界颜色
        .add(series_name="yichart", data_pair=data1, type_=GeoType.EFFECT_SCATTER)  # 设置地图数据，动画方式为涟漪特效effect scatter
        .set_series_opts(  # 设置系列配置
        label_opts=opts.LabelOpts(is_show=False),  # 不显示Label
        effect_opts=opts.EffectOpts(scale=5))  # 设置涟漪特效缩放比例
        .set_global_opts(  # 设置全局系列配置
        visualmap_opts=opts.VisualMapOpts(min_=0, max_=sum / len(data1), is_show=True),  # 设置视觉映像配置，最大值为平均值
        title_opts=opts.TitleOpts(title="全国疫情地图", subtitle=china_total, pos_left="center", pos_top="10px",
                                  title_textstyle_opts=opts.TextStyleOpts(color="#fff")),  # 设置标题，副标题，标题位置，文字颜色
        legend_opts=opts.LegendOpts(is_show=False),  # 不显示图例
    )
)

geo.render(path="./全国疫情图.html")
