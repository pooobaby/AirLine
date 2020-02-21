#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright By Eric in 2020

"""
从feiji123.com获取全国航线，并生成JSON格式的数据文件，以便用于可视化处理
"""
import re
import lxml
import json
import requests
from bs4 import BeautifulSoup


class AirLineData(object):
    def __init__(self):
        self.url = 'http://www.feiji123.com/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'
        }
        self.filename = 'airline.json'

    def getData(self):
        reps = requests.get(url=self.url, headers=self.headers)
        reps = reps.text.encode("latin1").decode("gbk")     # 转换网页编码为utf-8
        soup = BeautifulSoup(reps, 'lxml')
        line_all = soup.find_all(class_='tb1')
        city_dict = {}
        for line in line_all[3:-1]:
            city_tds = line.find_all('td')
            start_city_name = city_tds[0].find('a').string
            start_city_abbr = re.search('[A-Z]+', city_tds[0].text, re.S)[0]    # 用正则将城市代码析出
            start_city = [start_city_name, start_city_abbr]     # 出发城市与代码
            cities = city_tds[1].text.replace('\n', '').replace('\t', '').split('\r')
            end_city = []
            for city in cities:
                if city:
                    cc = city.split('(')
                    end_city.append((cc[0], cc[1].replace(')', '')))        # 到达城市与航班数量
            city_dict.update({start_city[1]: {"start": start_city[0], "end": end_city}})
        return city_dict

    def saveData(self, data):
        city_json = json.dumps(data, ensure_ascii=False)
        pdb.set_trace()
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(city_json)
        return


def main():
    air_line_data = AirLineData()
    data = air_line_data.getData()      # 将爬取的数据整理后生成dict数据
    air_line_data.saveData(data)        # dict数据转换为json后保存到文件中


if __name__ == '__main__':
    main()
