import concurrent.futures
import time

import requests
import urllib3
from bs4 import BeautifulSoup


class IPUtil:
    site_map = {
        "bsc-faucet": "https://testnet.bnbchain.org/faucet-smart"
    }

    def __init__(self):
        self.ips = []

    @staticmethod
    def site1_extract_ip(urlx):
        time.sleep(1)
        ips = []
        session = requests.Session()
        response = session.get(urlx)
        soup = BeautifulSoup(response.text, 'html.parser')
        ip_table = soup.find('tbody')
        rows = ip_table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 0 or len(columns) == 1:
                continue
            ip_address = columns[0].text.strip()
            port = columns[1].text.strip()
            # country = columns[2].find('span', class_='table-country').text.strip()
            dl_type = columns[5].text.strip()
            # 使用多线程并发检查代理IP是否有效
            dl = f'{dl_type}://{ip_address}:{port}'
            ips.append(dl)
        print(f"{ips}")
        return ips

    @staticmethod
    def site2_extract_ip(urlx):
        time.sleep(1)
        ips = []
        session = requests.Session()
        response = session.get(urlx, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        ip_table = soup.find('tbody')
        rows = ip_table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 0 or len(columns) == 1:
                continue
            ip_address = columns[0].text.strip()
            port = columns[1].text.strip()
            # country = columns[2].find('span', class_='table-country').text.strip()
            dl_type = str(columns[3].text).lower().strip()
            dl = f'{dl_type}://{ip_address}:{port}'
            ips.append(dl)
        print(f"{ips}")
        return

    @staticmethod
    def site3_extract_ip(urlx):
        time.sleep(1)
        ips = []
        session = requests.Session()
        response = session.get(urlx)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('.bg tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 0 or len(columns) == 7:
                continue
            ip_address = columns[1].text.strip()
            port = columns[2].text.strip()
            # country = columns[2].find('span', class_='table-country').text.strip()
            dl_type = 'http'
            dl = f'{dl_type}://{ip_address}:{port}'
            ips.append(dl)
        print(f"{ips}")
        return ips

    @staticmethod
    def collect_ip_pool1(out_path):
        """
        代理网址1:https://www.freeproxy.world
        """
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        results = []
        urls = [f'https://www.freeproxy.world/?type=&anonymity=&country=&speed=1500&port=&page={page + 1}' for page in range(0, 11)]
        # 获取所有网址上的代理
        for page_url in urls:
            future = executor.submit(IPUtil.site1_extract_ip, page_url)
            results.append(future)
        concurrent.futures.wait(results)
        return IPUtil.check_and_save_ok_ip(results, out_path)

    @staticmethod
    def collect_ip_pool2(out_path):
        """
        代理网址2 https://ip.jiangxianli.com/
        """
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        results = []
        urls = [f'https://ip.jiangxianli.com/?page={page + 1}' for page in range(0, 4)]
        for page_url in urls:
            future = executor.submit(IPUtil.site2_extract_ip, page_url)
            results.append(future)
        concurrent.futures.wait(results)
        return IPUtil.check_and_save_ok_ip(results, out_path)

    @staticmethod
    def collect_ip_pool3(out_path):
        """第三个代理网站"""
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        results = []
        urls = [f'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{page + 1}' for page in range(0, 6)]
        for page_url in urls:
            future = executor.submit(IPUtil.site3_extract_ip, page_url)
            results.append(future)
        concurrent.futures.wait(results)
        return IPUtil.check_and_save_ok_ip(results, out_path)

    @classmethod
    def collect_ip_pool4(cls, out_path):
        """第4个代理网站"""
        url = "http://list.sky-ip.net/user_get_ip_list?token=jax0WpZvQb4WPdLU1669392891594&qty=500&country=&time=5&format=json&protocol=http"
        resp = requests.get(url)
        results = [f'http://{ip}' for ip in resp.json()["data"]]
        return IPUtil.check_ips(results, out_path)

    #
    # def collect_ip_pool4():
    #     """
    #     第四个个 http://www.kxdaili.com/dailiip/1/2.html
    #     """
    #     executor = concurrent.futures.ThreadPoolExecutor(max_workers=25)
    #     for type in range(2):
    #         for page in range(10):
    #             url = f'http://www.kxdaili.com/dailiip/{type + 1}/{page + 1}.html'
    #             print(f'冲{type + 1}-第{page + 1}页！！！！')
    #             session = requests.Session()
    #             response = session.get(url)
    #             soup = BeautifulSoup(response.text, 'html.parser')
    #             rows = soup.select('tbody')
    #             for row in rows:
    #                 columns = row.find_all('td')
    #                 if len(columns) == 0 or len(columns) == 7:
    #                     continue
    #                 ip_address = columns[0].text.strip()
    #                 port = columns[1].text.strip()
    #                 # country = columns[2].find('span', class_='table-country').text.strip()
    #                 dl_type = 'http'
    #                 # 使用多线程并发检查代理IP是否有效
    #                 executor.submit(check_proxy, dl_type, ip_address, port)
    #
    # def collect_ip_pool5():
    #     """
    #     第五个 https://proxy.ip3366.net/free/?action=china&page=1
    #     """
    #     executor = concurrent.futures.ThreadPoolExecutor(max_workers=25)
    #     executor2 = concurrent.futures.ThreadPoolExecutor(max_workers=25)
    #     executor3 = concurrent.futures.ThreadPoolExecutor(max_workers=25)
    #     for page in range(200):
    #         url = f'https://proxy.ip3366.net/free/?action=china&page=1https://proxy.ip3366.net/free/?action=china&page={page + 1}'
    #         print(f'冲第{page + 1}页！！！！')
    #         session = requests.Session()
    #         response = session.get(url)
    #         soup = BeautifulSoup(response.text, 'html.parser')
    #         rows = soup.select('tbody')
    #         for row in rows:
    #             columns = row.find_all('td')
    #             if len(columns) == 0 or len(columns) == 7:
    #                 continue
    #             ip_address = columns[0].text.strip()
    #             port = columns[1].text.strip()
    #             # country = columns[2].find('span', class_='table-country').text.strip()
    #             dl_type = str(columns[3].text).lower().strip()
    #             # 使用多线程并发检查代理IP是否有效
    #             executor.submit(check_proxy, dl_type, ip_address, port)
    #             executor2.submit(check_proxy1, dl_type, ip_address, port)
    #             executor3.submit(check_proxy2, dl_type, ip_address, port)
    #
    # def collect_ip_pool6():
    #     """
    #     第六个 https://proxy.ip3366.net/free/?action=china&page=1
    #     """
    #     executor1 = concurrent.futures.ThreadPoolExecutor(max_workers=50)
    #     executor2 = concurrent.futures.ThreadPoolExecutor(max_workers=50)
    #     for page in range(2000, 2041):
    #         url = f'https://www.xsdaili.cn/dayProxy/ip/{page}.html'
    #         print(f'冲第{page}页！！！！')
    #         session = requests.Session()
    #         response = session.get(url)
    #         soup = BeautifulSoup(response.text, 'html.parser')
    #         all_br = soup.select_one('.cont').find_all('br')
    #         for br in all_br:
    #             row = br.next_sibling.text.strip()
    #             if not row:
    #                 continue
    #             info = row.split("@")
    #             # print(info)
    #             ip_address = info[0].split(":")[0]
    #             port = info[0].split(":")[1]
    #             # country = columns[2].find('span', class_='table-country').text.strip()
    #             dl_type = "http"
    #             # 使用多线程并发检查代理IP是否有效
    #             executor1.submit(check_proxy, dl_type, ip_address, port)
    #             executor2.submit(check_proxy1, dl_type, ip_address, port)
    #
    # def collect_ip_pool7():
    #     """
    #     第7个  "https://www.89ip.cn/index_1.html"
    #     """
    #     executor1 = concurrent.futures.ThreadPoolExecutor(max_workers=50)
    #     executor2 = concurrent.futures.ThreadPoolExecutor(max_workers=50)
    #     for page in range(47):
    #         url = f'https://www.89ip.cn/index_{page + 1}.html'
    #         print(f'冲第{page}页！！！！')
    #         session = requests.Session()
    #         response = session.get(url)
    #         soup = BeautifulSoup(response.text, 'html.parser')
    #         rows = soup.select_one('tbody').find_all('tr')
    #         for row in rows:
    #             info = row.find_all('td')
    #             if not row:
    #                 continue
    #             ip_address = info[0].text.strip()
    #             port = info[1].text.strip()
    #             # country = columns[2].find('span', class_='table-country').text.strip()
    #             dl_type = "http"
    #             # 使用多线程并发检查代理IP是否有效
    #             executor1.submit(check_proxy, dl_type, ip_address, port)
    #             executor2.submit(check_proxy1, dl_type, ip_address, port)
    #
    # def collect_ip_pool8():
    #     """
    #     第8个 http://www.66ip.cn/2.html
    #     """
    #     executor1 = concurrent.futures.ThreadPoolExecutor(max_workers=50)
    #     executor2 = concurrent.futures.ThreadPoolExecutor(max_workers=50)
    #     for page in range(2000, 3015):
    #         url = f'http://www.66ip.cn/{page + 1}.html'
    #         print(f'冲第{page}页！！！！')
    #         session = requests.Session()
    #         response = session.get(url)
    #         soup = BeautifulSoup(response.text, 'html.parser')
    #         rows = soup.select_one('#main').find_all('tr')
    #         for row in rows:
    #             info = row.find_all('td')
    #             if info[0].text == "ip":
    #                 continue
    #             ip_address = info[0].text.strip()
    #             port = info[1].text.strip()
    #             # country = columns[2].find('span', class_='table-country').text.strip()
    #             dl_type = "http"
    #             # 使用多线程并发检查代理IP是否有效
    #             executor1.submit(check_proxy, dl_type, ip_address, port)
    #             executor2.submit(check_proxy1, dl_type, ip_address, port)

    @staticmethod
    def check_and_save_ok_ip(results, out_path):
        valid_ips = list(filter(lambda x: x is not None, [x.result() for x in results]))
        valid_ips = [item for sublist in valid_ips for item in sublist]
        executor2 = concurrent.futures.ThreadPoolExecutor(max_workers=50)
        results2 = []
        for ht in valid_ips:
            result = executor2.submit(IPUtil.check_ip, ht)
            results2.append(result)
        concurrent.futures.wait(results2)
        # 验证过后可用的代理
        xs = [x.result() for x in results2]
        valid_ips2 = list(filter(lambda x: x is not None, xs))
        IPUtil.save_ips(valid_ips2, out_path)
        return valid_ips2

    @staticmethod
    def check_ips(ips, out_path):
        valid_ips = ips
        executor2 = concurrent.futures.ThreadPoolExecutor(max_workers=50)
        results2 = []
        for ht in valid_ips:
            result = executor2.submit(IPUtil.check_ip, ht)
            results2.append(result)
        concurrent.futures.wait(results2)
        # 验证过后可用的代理
        xs = [x.result() for x in results2]
        valid_ips2 = list(filter(lambda x: x is not None, xs))
        IPUtil.save_ips(valid_ips2, out_path)
        return valid_ips2

    @staticmethod
    def check_ip(ip):
        proxy = {'http': f'{ip}', 'https': f'{ip}'}
        try:
            session1 = requests.Session()
            response = session1.get(check_url, proxies=proxy, timeout=5, verify=False)
            # if response.status_code in [200, 403]:
            # and "DOCTYPE HTML" not in response.text.upper():
            print("可用的ip", ip)
            return ip
        except Exception as e:
            print("失效的ip", ip)
            return None

    @staticmethod
    def is_ip_valid(ip):
        proxy = {'http': f'{ip}', 'https': f'{ip}'}
        try:
            url = "https://testnet.bnbchain.org/faucet-smart"
            response = requests.Session().get(url, proxies=proxy, timeout=5, verify=False)
            if response.status_code in [200, 403]:
                print(ip)
                return True
            return False
        except Exception as e:
            return False

    @staticmethod
    def check_ip_from_file(file_path):
        file_data = open(file_path, 'r').readlines()  # 打开文件
        executor1 = concurrent.futures.ThreadPoolExecutor(max_workers=200)
        results = []
        for i, row in enumerate(file_data, start=1):
            info = row.split('|')  # 按‘----’切分每行的数据
            ip_address = info[0].strip()
            port = info[1].strip()
            # country = columns[2].find('span', class_='table-country').text.strip()
            dl_type = "socks5"
            username = info[2]
            password = info[3]
            result = executor1.submit(IPUtil.check_proxy, dl_type, ip_address, port, username, password)
            results.append(result)
        concurrent.futures.wait(results)
        ips = [x.result() for x in results]
        valid_ips = list(filter(lambda x: x is not None, ips))
        IPUtil.save_ips(valid_ips, file_path)

    @staticmethod
    def save_ips(valid_ips, file_path):
        with open(f'{file_path}_有效ip.txt', 'a+') as f:
            for ip in valid_ips:
                f.write(ip + '\n')
            f.close()

    @staticmethod
    def check_proxy(ip_type, ip, port, username=None, password=None):
        """
        带账户密码的代理
        """
        if username:
            dl = f'{ip_type}://{username}:{password}@{ip}:{port}'
            proxy = {'http': f'{dl}', 'https': f'{dl}'}
        else:
            dl = f'{ip_type}://{ip}:{port}'
            proxy = {'http': f'{dl}', 'https': f'{dl}'}
        try:
            session1 = requests.Session()
            response = session1.get(check_url, proxies=proxy, timeout=8, verify=False)
            # if response.status_code in [200, 403]:
            print(f'正常的ip: {dl}')
            return dl
        except Exception as e:
            print(f'失效的ip: {dl}')
            return None



if __name__ == '__main__':
    urllib3.disable_warnings()
    check_url = "https://artio-80085-faucet-api-recaptcha.berachain.com/api/claim"
    # IPUtil.check_ip_from_file("sock5-5000.txt")
    # IPUtil.collect_ip_pool1("网站1可用代理-0203-1.txt")
    # IPUtil.collect_ip_pool2("网站2可用代理-0203-1.txt")
    # IPUtil.collect_ip_pool3("网站3可用代理-0203-1.txt")
    IPUtil.collect_ip_pool4("sky-ip可用代理-0205-1.txt")
