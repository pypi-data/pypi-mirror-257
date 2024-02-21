import hashlib
from urllib.parse import urlparse, parse_qs
import yaml
import csv

class QGUtil:
    @staticmethod
    def save_to_file(file_path, log):
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f'{log}\n')
            f.close()

    @staticmethod
    def txt_to_array(file_path: object, split: object = '----') -> list:
        lines = open(file_path, 'r', encoding='utf-8').readlines()
        arr = [[z.strip() for z in x.split(split)] for x in lines]
        return arr

    @staticmethod
    def array_to_txt(arr, to_file_path) -> list:
        with open(to_file_path, 'a', encoding='utf-8') as f:
            for cols in arr:
                log = "----".join(cols)
                f.write(f'{log}\n')
            f.close()
        lines = open(to_file_path, 'r', encoding='utf-8').readlines()
        arr = [[z.strip() for z in x.split(to_file_path)] for x in lines]
        return arr

    @staticmethod
    def read_yaml(file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def url_params_to_object(url):
        # 解析URL
        parsed_url = urlparse(url)
        # 获取查询字符串参数并转换为字典对象
        query_params = parse_qs(parsed_url.query)
        # 处理字典对象，将每个参数的值转换为单个值而不是数组
        for key, value in query_params.items():
            query_params[key] = value[0]
        # 返回转换后的字典对象
        return query_params

    @staticmethod
    def csv_to_array(file_path, has_header=True, delimiter=','):
        """解汇csv文件，返回数组对象"""
        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=delimiter)
            all_list = list(reader)
            if len(all_list) == 0:
                return []
            if has_header:
                head_list = all_list[0]
                data_list = all_list[1:]
                array_obj = []
                for data in data_list:
                    obj = {}
                    for i, attr in enumerate(head_list, start=0):
                        obj[attr] = data[i]
                    array_obj.append(obj)
                # print(array_obj)
                return array_obj
            else:
                return all_list

    @staticmethod
    def to_yaml(wallet_path, dis_path, tw_path, to_path):
        """往文件修改新增"""
        wallets = QGUtil.csv_to_array(wallet_path)
        # wallets = QGUtil.txt_to_array(wallet_path)
        dis_tokens = QGUtil.txt_to_array(dis_path)
        tws = QGUtil.txt_to_array(tw_path)
        full_data = {
            "accounts": []
        }
        for i, row in enumerate(wallets, start=0):
            addr1 = row.get("addr")
            pk1 = row.get("pk")
            if i <= 21:
                continue
            else:
                obj = {
                    "address": f"{addr1}",
                    "private_key": f"{pk1}",
                    "email": "",
                    "twitter": {
                        "username": f"",
                        "auth_token": f"",
                        "ct0": f"",
                    },
                    "discord": {
                        "username": "kukjaobicip774#9913",
                        "token": "MTA3ODE0MDE4NTQ3ODQ0MzEwOQ.GY6eT9.r6D7H7-"
                    }
                }
                full_data['accounts'].append(obj)
        with open(to_path, 'w') as file:
            yaml.dump(full_data, file)
        print("数据已成功修改并写回到YAML文件。")

    @staticmethod
    def save_to_yaml(to_path, full_data):
        with open(to_path, 'w') as file:
            yaml.dump(full_data, file)
        print("数据已成功修改并写回到YAML文件。")

    @staticmethod
    def md5_hash(text):
        md5_hasher = hashlib.md5()
        md5_hasher.update(text.encode('utf-8'))
        return md5_hasher.hexdigest()

    @staticmethod
    def sha256_hash(text):
        sha256_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        return sha256_hash

    @staticmethod
    def google_author(secret_key):
        import pyotp
        import time
        # 替换为您的谷歌身份验证器密钥
        # secret_key = f"{self.phone}"
        # 创建一个TOTP对象
        totp = pyotp.TOTP(secret_key)
        # 获取当前时间戳
        current_time = int(time.time())
        # 获取谷歌验证码
        otp = totp.at(current_time)
        # 获取谷歌验证码的有效期剩余秒数
        remaining_seconds = totp.interval - (current_time % totp.interval)
        print(f"谷歌验证码:{otp}", f"有效期剩余秒数:{remaining_seconds}")


if __name__ == '__main__':
    # # QGUtil.to_yaml("Taki100.csv", "dis正常token账号0814-1.txt", "../wallets/twitter/tw400-1.txt", "23-100.yaml")
    # accounts = QGUtil.read_yaml("23-100-2.yaml")
    # tws = QGUtil.txt_to_array("../wallets/twitter/tw_google_79_提取结果.txt")
    # dis = QGUtil.txt_to_array("dis正常token账号0814-1.txt")
    # for i, account in enumerate(accounts['accounts'], start=1):
    #     if i == 1:
    #         continue
    #     if i <= 11:
    #         continue
    #     tk_info1 = ast.literal_eval(tws[i - 12][4].strip())
    #     account["twitter"]["username"] = tws[i - 12][1].strip()
    #     account["twitter"]["auth_token"] = tk_info1["auth_token"]
    #     account["twitter"]["ct0"] = tk_info1["ct0"]
    #     # account["discord"]["token"] = dis[i + 21][1].strip()
    #     # account["discord"]["username"] = dis[i+21][2].strip()
    #
    # print(accounts)
    # with open("23-100-2.yaml", 'w') as file:
    #     yaml.dump(accounts, file)
    # # QGUtil.csv_to_array("Taki100.csv")
    QGUtil.google_author("SGP6AGDUJAJRYJ54")
