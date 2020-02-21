#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright By Eric in 2020

"""
从JSON数据文件中取得数据，调用地理编码程序生成自定义经纬度坐标，
按出发城市生成可视化地图
"""

import json
from position import Position
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType


class AirLineMap(object):
    def __init__(self):
        self.name = '西安'        # 在这里修改城市名称
        self.filename = 'airline.json'      # 调用的数据文件名称

    def cleanData(self):
        print('开始处理%s中的数据......' % self.filename)
        with open(self.filename, 'r', encoding='utf-8') as f:      # 打开json数据文件
            data_all = f.read()
        data_all = json.loads(data_all)
        data_list, city_list, city_name = [], [], []
        for city_abbr in data_all:
            for data in data_all[city_abbr]['end']:
                city_list.append((data_all[city_abbr]['start'],
                                  len(data_all[city_abbr]['end'])))    # 城市名称与航班数量
                data_list.append((data_all[city_abbr]['start'], data[0]))       # 出发与到达城市列表
                city_name.append(data[0])       # 用于地理编码的城市列表
        city_name = list(set(city_name))        # 数据去重处理
        city_list = list(set(city_list))        # 数据去重处理
        return [city_list, data_list, city_name]

    def cityName(self, data):
        lines = []
        for i in data[1]:       # 在航线数据中筛选指定城市的数据
            if i[0] == self.name:
                lines.append(i)     # 生成指定城市的数据
        return lines

    def makeMap(self, data, lines) -> Geo:
        count = len(lines)
        c = (
            Geo(init_opts=opts.InitOpts(width='1000px', height='500px'))
            .add_schema(maptype="china", zoom=1.1)
            .add_coordinate_json('positions.json')
            .add("", data, symbol_size=6, color='#725e82')      # 标记点大小与颜色
            .add("", lines, type_=ChartType.LINES,
                 linestyle_opts=opts.LineStyleOpts(curve=0.1, width=1, color='#1685a9'),    # 连线的宽度与颜色
                 effect_opts=opts.EffectOpts(is_show=False))    # 关闭涟漪效果
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="【%s】民航班机航线图" % self.name,
                             subtitle='{}共有直飞全国{}个城市的航班'.format(self.name, count))))
        return c


def main():
    html_filename = 'airline.html'
    air_line_map = AirLineMap()
    position = Position()       # 调用position库中的模块实例化对象
    data = air_line_map.cleanData()     # 对json文件中的数据清洗
    position.saveData(data[2])      # 对城市数据进行地理编码
    lines = air_line_map.cityName(data)     # 按指定城市生成航线数据
    air_line_map.makeMap(data[0], lines).render(html_filename)     # 生成可视化地图
    print('可视化地图生成完毕，请在浏览器中打开文件：%s' % html_filename)


if __name__ == '__main__':
    main()
