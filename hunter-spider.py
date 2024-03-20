import requests
import openpyxl
import hashlib
import json
import base64
import datetime
import logging
import sys
import argparse
import time

logger = logging.getLogger()  # 获取日志
logger.setLevel(logging.INFO) # 设置日志级别
logger.addHandler(logging.StreamHandler(sys.stdout))

class BreakLoop(Exception):
    pass

class HunterApi:
    def __init__(self, api_key, interval=3):
        self.api_key = api_key # 初始化获取hunter API
        self.interval = int(interval) # 默认请求间隔3秒

    def getdata(self, rule: str, page: int, page_size: int):
        search_rule = base64.urlsafe_b64encode(rule.encode())

        url = f'https://hunter.qianxin.com/openApi/search'
        params = {
            'api-key': self.api_key,
            'search': search_rule.decode(),
            'page': page,
            'page_size': page_size
        }
        
        try:
            r = requests.get(url, params=params)
            return r.json()
        except Exception as e:
            logger.error(f'[!] 请求hunter接口出现问题: {str(e)}')
            return {}

    def crawler(self, rule: str, sheet, page_size: int=100, start_page: int=1, end_page: int=None):
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_time = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
        page_index = start_page
        try:
            while True:
                if end_page is not None and page_index > end_page:
                    break
                resp_data = self.getdata(rule, page_index, page_size)
                if resp_data.get('code') != 200:
                    logger.info(f'[!] [hunterApi] {rule} 爬取第 {page_index} 页时出错: {json.dumps(resp_data, ensure_ascii=False)}')
                    break

                ipdata_list = resp_data.get('data', {}).get('arr', [])
                if not ipdata_list:
                    logger.info(f'[v] [hunterApi] {rule} 爬取数据完成')
                    break

                for ipdata in ipdata_list:
                    try:
                        if not (ipdata.get("ip") and ipdata.get('port')):
                            continue

                        web_title_icon = b''
                        try:
                            web_title_icon = base64.b64decode(ipdata.get('web_title_icon', ''))
                        except:
                            pass
                        
                        ipport = f'{str(ipdata.get("ip", "")).strip()}:{str(ipdata.get("port", "")).strip()}'
                        protocol = ipdata.get('protocol')
                        web_title = ipdata.get('web_title')
                        domain = ipdata.get('domain')
                        url = ipdata.get('url')
                        status_code = ipdata.get('status_code')
                        updated_at = ipdata.get('updated_at')
                        company = ipdata.get('company')
                        icp_number = ipdata.get('number')
                        region = ipdata.get('city')
                        region_all = f'{ipdata.get("country")}/{ipdata.get("province")}/{ipdata.get("city")}'

                        sheet.append([ipport, protocol, web_title, domain, url, status_code, updated_at, company, icp_number, region, region_all, web_title_icon])
                        logger.info(f'[*] 成功爬取数据: [{url}] [{web_title}] {ipport}')
                    except Exception as e:
                        logger.error(f'[!] 出现未知异常: {str(e)}')

                page_index += 1
                time.sleep(self.interval)

        except Exception as e:
            logger.error(f'[!] 出现未知异常: {str(e)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--apikey', type=str, help='hunter api key', required=True)
    parser.add_argument('--start_page', default=1, type=int, help='爬取开始页数', required=False)
    parser.add_argument('--end_page', default=None, type=int, help='爬取结束页数，默认为一直爬取，直至积分不够或者爬取完成', required=False)
    parser.add_argument('--page_size', default=100, type=int, help='每页爬取数量，最大为100', required=False)
    parser.add_argument('--txt', type=str, help='包含单位名称的txt文件路径', required=True)
    parser.add_argument('--interval', default=3.0, type=float, help="每次请求api之间的时间间隔", required=False)
    args = parser.parse_args()

    units = []
    with open(args.txt, 'r', encoding='utf-8') as file:
        units = file.readlines()

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["IP端口", "协议", "网站标题", "域名", "URL", "状态码", "更新时间", "公司", "ICP号", "地区", "全地区", "网站标题图标"])

    hunter = HunterApi(args.apikey, interval=args.interval)

    for unit in units:
        rule = f'icp.web_name="{unit.strip()}"' #设置查询语句
        logger.info(f'开始扫描单位: {unit.strip()}')
        hunter.crawler(rule, sheet, args.page_size, args.start_page, args.end_page)

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    workbook.save(f"assets_info_{timestamp}.xlsx")
    logger.info(f"成功保存数据到 assets_info_{timestamp}.xlsx")
