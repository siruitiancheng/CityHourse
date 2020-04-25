import requests
import base64
import pandas as pd
from city_level import one,two,three
from log import logger
from lxml import etree
from proxy_ip import proxies
import time


pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',1000)


class ConPowerAnalysis():

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "cityre=e6ba2db615a186ff74f49716b58e98b4; city=http%3A//bj.cityhouse.cn; Hm_lvt_435bf6d47bee0643980454513deeb34f=1587386307,1587439345,1587546711,1587561644; Hm_lpvt_435bf6d47bee0643980454513deeb34f=1587616035",
        "Host": "m.cityhouse.cn",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
    }

    def __init__(self):
        self.__file = '数据.xlsx'
        self.__url = "http://m.cityhouse.cn/beijing/default/search.html?s="


    def add_city_level(self):
        pd_excel = pd.read_excel(self.__file)
        pd_excel = pd_excel.groupby(["省份","市","区","详细地址"]).sum()
        pd_excel = pd_excel.reset_index(level=[0,1,2,3])
        pd_excel['城市级别'] = ""
        for i in range(0, len(pd_excel["市"])):
            if pd_excel["市"][i] in one:
                pd_excel.loc[i, "城市级别"] = "一级城市"
            elif pd_excel["市"][i] in two:
                pd_excel.loc[i, "城市级别"] = "二级城市"
            elif pd_excel["市"][i] in three:
                pd_excel.loc[i, "城市级别"] = "三级城市"
            else:
                pd_excel.loc[i, "城市级别"] = "四级及以下城市"
        return pd_excel


    def get_detail_adder(self):
        pd_excel = ConPowerAnalysis().add_city_level()
        pd_detil_addr = list(pd_excel['详细地址'])
        return pd_detil_addr


    def get_hourse_detail_url(self):
        hourse_avg = []
        heads_son = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
                                        "Cookie": "cityre=e6ba2db615a186ff74f49716b58e98b4; city=http%3A//bj.cityhouse.cn; Hm_lvt_435bf6d47bee0643980454513deeb34f=1587439345,1587546711,1587561644,1587616570; Hm_lpvt_435bf6d47bee0643980454513deeb34f=1587617992",
            "Host": "m.cityhouse.cn",
            "Referer": "http://m.cityhouse.cn/beijing/ha/pa0150429ft762.html",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        addrs = ConPowerAnalysis().get_detail_adder()
        for addr in addrs:
            if type(addr) != str:
                addr = str(addr)
            url = self.__url + addr
            logger.info("1.输入请求为：{}".format(url))
            time.sleep(1)
            res = requests.get(url=url, headers=ConPowerAnalysis.headers,proxies=proxies,stream=True)
            data = res.text
            data = data.replace(r'<!--', '"').replace(r'-->', '"')
            txt = etree.HTML(data)
            try:
                not_find = txt.xpath('//div[@class="dfsearch_title"]//text()')
                if not_find == "未查询到记录":
                    hourse_avg.append("未查询到记录")
                    logger.info("3.未查询到改小区均价为")

                else:
                    is_find_url = txt.xpath("//div[@class='dfsearch_list']/ul/li[1]/a/@href")
                    detail_urls = ''.join(is_find_url)
                    logger.info("2.详细页面地址URL为：{}".format(url))
                    time.sleep(1)
                    respon = requests.get(url=detail_urls,headers = heads_son,proxies=proxies,stream=True).text
                    respon = respon.replace(r'<!--', '"').replace(r'-->', '"')
                    txt = etree.HTML(respon)
                    price =  txt.xpath('//div[@class="title_price"]/ul/li[1]/span[@class="r_unit"]//text()')
                    price = ''.join(price)
                    logger.info("3.小区{}的均价为：{}".format(addr,price))

                    hourse_avg.append(price)
            except Exception:
                try:
                    price =  txt.xpath('//div[@class="title_price"]/ul/li[1]/span[@class="r_unit"]//text()')
                    price = ''.join(price)
                    hourse_avg.append(price)
                    logger.info("3.小区{}的均价为：{}".format(addr, price))
                except Exception:
                    hourse_avg.append("暂无均价")
                    logger.info("暂无均价")
        series_addrs = pd.Series(data=hourse_avg)
        add_hourse_avg = ConPowerAnalysis().add_city_level()
        add_hourse_avg['小区均价'] = series_addrs
        add_hourse_avg.to_excel('./新表.xlsx')
        return hourse_avg


if __name__ == '__main__':
    ConPowerAnalysis().get_hourse_detail_url()















