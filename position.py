#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright By Eric in 2020
"""
利用高德地图API生成地理编码程序，可以在程序中做为类引用
输入:列表格式 list=['北京市朝阳区'，'上海市普陀区真如寺', '沈阳市'...]
输出:在当前目录下生成JSON格式的文件，并返回同值的字典数据
    文件名称：positions.json
    文件内容：列表格式 "深圳": [114.057868, 22.543099], "普洱": [100.966512, 22.825065]...
注意：当地址不明确或不正确时，坐标列表将生成null，使用时请注意筛选。
"""

import json
import requests
from tqdm.std import trange


class Position(object):
    def __init__(self):
        self.key = '高德地图API的key'       # 高德地图API的key
        self.filename = 'positions.json'

    def location(self, address):
        url_loc = 'https://restapi.amap.com/v3/geocode/geo?address=' + \
                  address + '&key=' + self.key
        req = requests.get(url_loc)
        data = json.loads(req.text)
        if data['count'] == '0':  # 过滤不能生成地理位置坐标的数据
            return
        pos = data['geocodes'][0]['location'].split(',')
        if float(pos[0]) == 0 or float(pos[1]) == 0:  # 去除坐标值为0的数据
            return
        pos_lon_lat = [float(pos[0]), float(pos[1])]
        return pos_lon_lat

    def saveData(self, data):
        print('开始进行地理位置编码......')
        pos_dict = {}
        for n in trange(len(data)):
            pos_lon_lat = self.location(data[n])
            pos_dict.update({data[n]: pos_lon_lat})
        json_data = json.dumps(pos_dict, ensure_ascii=False)
        with open(self.filename, 'w', encoding='utf-8') as f:        # 将结果存储为JSON文件
            f.write(json_data)
        print('地理位置编码完成，生成文件：%s' % self.filename)
        return pos_dict
