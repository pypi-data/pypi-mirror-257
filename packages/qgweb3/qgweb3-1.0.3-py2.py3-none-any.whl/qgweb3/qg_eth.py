import base64
import binascii
import inspect
import json
import random
from decimal import Decimal
from pathlib import Path
from threading import Lock

import requests
from eth_account import Account
from eth_account.messages import encode_defunct, encode_structured_data
from retry import retry
from web3 import Web3
from web3.auto import w3

from logging_utils import log_info


class QGEth:
    # rpc

    endpoints = {
        "mainnet": "https://mainnet.infura.io/v3/257c5f3bdfed414b88a4908b0f999377",
        # "bsc": "https://data-seed-prebsc-1-s1.binance.org:8545",
        # "bsc": 'https://1gwei.48.club',
        "bsc": "https://rpc.ankr.com/bsc",
        # "bsc": "https://bsc.blockpi.network/v1/rpc/eee28a206a110cf0d0b58371cfbfae4ee5864bfb",
        # "bsc": "https://go.getblock.io/4f453487a0f4424f82b7bb2e0026e8d4",
        # "bsc": "https://bsc.blockpi.network/v1/rpc/public",
        # "bsc": "https://bsc-dataseed2.defibit.io",
        "goerli": "https://eth-goerli.g.alchemy.com/v2/hLTAisSN98aFruQM7qYQC8EBP4tjfymv",
        # "goerli": "https://goerli.blockpi.network/v1/rpc/public",
        # "goerli": "https://ethereum-goerli.publicnode.com",
        # "goerli": "https://goerli.gateway.tenderly.co",
        # "goerli": "https://eth-goerli.public.blastapi.io",
        # "goerli": "https://eth-goerli.api.onfinality.io/public",
        "sepolia": "https://rpc.sepolia.org",
        "linea": "https://linea.blockpi.network/v1/rpc/public",
        "linea_test": "https://rpc.goerli.linea.build",
        "scroll_test": "https://alpha-rpc.scroll.io/l2",
        # "scroll": "https://rpc.ankr.com/scroll",
        "scroll": "https://1rpc.io/scroll",
        # "scroll": "https://rpc-scroll.icecreamswap.com",
        "shib": "https://www.shibrpc.com",
        "taiko": "https://rpc.test.taiko.xyz",
        "taikol3": "https://rpc.l3test.taiko.xyz",
        "taiko_jolnir": "https://taiko-jolnir.blockpi.network/v1/rpc/public",
        "mantle": "https://rpc.mantle.xyz",
        "mantle_test": "https://rpc.ankr.com/mantle_testnet",
        # "base_goerli": "https://chain-proxy.wallet.coinbase.com?targetName=base-goerli"
        "base_goerli": "https://goerli.base.org",
        "zora": "https://testnet.rpc.zora.co",
        "omni": "https://testnet-1.omni.network",
        "base": "https://developer-access-mainnet.base.org",
        "combo": "https://test-rpc.combonetwork.io",
        "zeta": "https://zetachain-evm.blockpi.network/v1/rpc/public",
        "zeta2": "https://api.athens2.zetachain.com/evm",
        "zeta3": "https://rpc.ankr.com/zetachain_evm_athens_testnet",
        "bsc_test": "https://data-seed-prebsc-1-s1.binance.org:8545/",
        "opbnb": "https://opbnb-mainnet-rpc.bnbchain.org",
        # "polygon": "https://rpc.ankr.com/polygon",
        "polygon": "https://polygon-bor.publicnode.com",
        # "polygon": "https://polygon-rpc.com",
        # "polygon": "https://polygon-mainnet.infura.io/v3/e033cdd0b4464967924989bbdcf18e12",
        "heco": "https://http-mainnet-node.huobichain.com",
        "ftm": "https://rpc3.fantom.network",
        "etc": "https://etc.rivet.link",
        # "etc": "https://etc.mytokenpocket.vip",
        # "etc": "https://etc.etcdesktop.com",
        # "etc": "https://besu-at.etc-network.info",
        "manta": "https://1rpc.io/manta",
        "arb": "https://arb1.arbitrum.io/rpc",
        # "arb": "https://arbitrum.blockpi.network/v1/rpc/public",
        # "arb": "https://arb-pokt.nodies.app",
        # "fil": "https://filecoin.chainup.net/rpc/v1",
        # "fil": 'https://filfox.info/rpc/v1',
        # "fil": "https://rpc.ankr.com/filecoin",
        # "fil": "https://node.filutils.com/rpc/v1",
        # "fil": "https://rpc.ankr.com/filecoin/3cdc25144192cd85f8d3cbfec024a46ec7442019996b70f7cfa368632f952641",
        "eos": "https://api.evm.eosnetwork.com",
        # "kcs": "https://kcc-rpc.com",
        # "kcs": "https://rpc-mainnet.kcc.network",
        # "kcs": "https://kcc-rpc.com",
        "kcs": "https://rpc-mainnet.kcc.network",
        # "kcs": "https://wallet.okex.org/priapi/v1/wallet/rpc/send?chainId=321"
        # "cfx": "https://evm.confluxrpc.com",
        # "cfx": "https://conflux-espace-public.unifra.io",
        "cfx": "https://cfx-espace.unifra.io/v1/271d5d84bd4b4344a56589e2db07f4f6",
        # "avav": "https://avalanche.blockpi.network/v1/rpc/public",
        # "avav": "https://rpc.ankr.com/avalanche",
        "avav": "https://avalanche.drpc.org",
        # "avav": "https://avax-pokt.nodies.app/ext/bc/C/rpc",
        "berachain": "https://artio.rpc.berachain.com",
        "kly": "https://public-en-cypress.klaytn.net",
        "blast": "https://sepolia.blast.io",
        "holesky": "https://l1rpc.katla.taiko.xyz"
    }

    # api接口
    bases = {
        "goerli": "https://api-goerli.etherscan.io/api",
        # "goerli": "https://eth-goerli.blockscout.com/api",
        "sepolia": "https://api-sepolia.etherscan.io/api",
        # "linea": "https://explorer.goerli.linea.build/api",
        "linea": "https://api-testnet.lineascan.build/api",
        "mantle": "https://explorer.mantle.xyz/api",
        "mantle_test": "https://explorer.testnet.mantle.xyz/api",
        "zora": "https://testnet.explorer.zora.energy/api",
        "omni": "https://testnet-1.explorer.omni.network/api",
        "bsc": "https://api.bscscan.com/api",
        "taiko": "https://explorer.test.taiko.xyz/api",
        "taikol3": "https://blockscoutapi.l3test.taiko.xyz/api",
        "combo": "https://api-combotrace-testnet.nodereal.io/api",
        "zeta": "https://zetachain.blockpi.network:443/rpc/v1/public/api",
        "zeta2": "https://rpc.ankr.com/http/zetachain_tendermint_athens_testnet/api",
        "zeta3": "https://zetachain-athens-evm.blockpi.network/v1/rpc/public/api",
        # "zeta3": "https://rpc.ankr.com/zetachain_evm_athens_testnet/995de8736b54e4c2b5ec62771fe384c27c9715835a9ccf0d0fd11c8eaf985095/api",
        "bsc_test": "https://api-testnet.bscscan.com/api",
        "opbnb": "https://opbnb-mainnet.nodereal.io/v1/b4876385e7ec46cd9da933f2a83d969c",
        "polygon": "https://api.polygonscan.com/api",
        "berachain": "https://api.routescan.io/v2/network/testnet/evm/80085/etherscan/api",
        "blast": "https://api.routescan.io/v2/network/testnet/evm/168587773/etherscan/api"
    }

    apis = {
        "get_account_tx_list": "?module=account&action=txlist&address={}",
        "get_tx_info": "?module=transaction&action=gettxinfo&txhash={}"
    }

    lock = Lock()

    def __init__(self, index, address, private_key=None, mnemonic=None):
        self.index = index
        self.address = Web3.to_checksum_address(address)
        # self.address = address
        self.private_key = private_key
        self.mnemonic = mnemonic
        self.chain_instances = {}

    @retry(tries=2, delay=1, backoff=1, max_delay=3)
    def init_chains(self, *chain_names):
        try:
            for name in chain_names:
                web3 = getattr(self, f"{name}_w3", None)
                if web3 is None:
                    self.add_chain(name)
                    self.add_balance(name)
            chains_info = []
            for chain_name, web3_instance in self.chain_instances.items():
                chains_info.append(f"{chain_name}余额:{self.get_balance_from_attr(chain_name)}")
            print(f"【{self.index}】【{self.address}】余额情况 {','.join(chains_info)}")
        except Exception as e:
            print(e)
            raise Exception("初始化失败！")

    def add_chain(self, chain_name):
        endpoint = self.endpoints.get(chain_name)
        if endpoint:
            web3 = Web3(Web3.HTTPProvider(endpoint))
            self.chain_instances[chain_name] = web3
            setattr(self, f"{chain_name}_w3", web3)

    def add_balance(self, chain_name):
        web3 = getattr(self, f"{chain_name}_w3", None)
        if web3:
            balance = Web3.from_wei(web3.eth.get_balance(self.address), 'ether')
            setattr(self, f"{chain_name}_balance", balance)

    def get_balance(self, chain_name, address=None):
        web3 = self.chain_instances.get(chain_name)
        if web3:
            if address:
                balance = Web3.from_wei(web3.eth.get_balance(address), 'ether')
            else:
                balance = Web3.from_wei(web3.eth.get_balance(self.address), 'ether')
            return balance
        else:
            return None

    def get_balance_from_web3(self, w3, addr):
        """获取指定地址的余额"""
        balance = Web3.from_wei(w3.eth.get_balance(addr), 'ether')
        return balance

    def get_balance_from_attr(self, chain_name):
        web3_balance = getattr(self, f"{chain_name}_balance", None)
        return web3_balance

    def get_token_balance(self, w3, contract_address):
        """
        查询指定代币的余额
        """
        balance_of_method_id = w3.keccak(text="balanceOf(address)").hex()[:10]
        data = balance_of_method_id + self.address.lower()[2:].zfill(64)
        token_balance = w3.eth.call({
            'to': Web3.to_checksum_address(contract_address),
            'data': data
        })
        hex_balance = binascii.hexlify(token_balance).decode()
        balance = Web3.from_wei(int(hex_balance, 16), 'wei')
        print(f'【{self.index}】【{self.address}】【合约代币：{contract_address}】余额：{balance}')
        return balance

    def get_token_by_w3(self, w3, to_address):
        """
        查询指定代币的余额
        """
        balance = Web3.from_wei(w3.eth.get_balance(Web3.to_checksum_address(to_address)), 'ether')
        print(f'【{self.index}】【{self.address}】余额：{balance}')
        return balance

    def get_token_balance_by_abi(self, w3, contract_address):
        ERC20_ABI = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function",
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function",
            },
        ]
        # 获取代币合约实例
        contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=ERC20_ABI)
        # 获取代币余额
        balance = contract.functions.balanceOf(Web3.to_checksum_address(self.address)).call()
        # 将余额转换为代币单位（以太为例，小数点18位）
        decimals = contract.functions.decimals().call()
        balance_in_units = balance / (10 ** decimals)
        print(f'【{self.address}】【合约代币：{contract_address}】余额：{balance_in_units}')
        return balance_in_units

    def get_that_token_balance_by_abi(self, w3, contract_address, addr):
        ERC20_ABI = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function",
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function",
            },
        ]
        # 获取代币合约实例
        contract = w3.eth.contract(address=contract_address, abi=ERC20_ABI)
        # 获取代币余额
        balance = contract.functions.balanceOf(Web3.to_checksum_address(addr)).call()
        # 将余额转换为代币单位（以太为例，小数点18位）
        decimals = contract.functions.decimals().call()
        balance_in_units = balance / (10 ** decimals)
        print(f'【{addr}】【合约代币：{contract_address}】余额：{balance_in_units}')
        return balance_in_units

    def get_token_by_w3_and_address(self, w3, contract_address, addr):
        abi_json = [{"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"},
                                                    {"indexed": False, "internalType": "address", "name": "to", "type": "address"},
                                                    {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
                                                    {"indexed": False, "internalType": "string", "name": "data", "type": "string"}],
                     "name": "CFXsCreated",
                     "type": "event"},
                    {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"}],
                     "name": "CFXsDeleted",
                     "type": "event"}, {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"},
                                                                       {"indexed": False, "internalType": "address", "name": "to", "type": "address"},
                                                                       {"indexed": False, "internalType": "uint256", "name": "amount",
                                                                        "type": "uint256"},
                                                                       {"indexed": False, "internalType": "string", "name": "data",
                                                                        "type": "string"}],
                                        "name": "CFXsEvent", "type": "event"}, {"anonymous": False, "inputs": [
                {"indexed": True, "internalType": "uint256", "name": "CFXsId", "type": "uint256"},
                {"indexed": False, "internalType": "uint256", "name": "etherAmount", "type": "uint256"},
                {"indexed": False, "internalType": "uint256", "name": "locktime", "type": "uint256"}], "name": "CFXsLocked", "type": "event"},
                    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "uint256", "name": "CFXsId", "type": "uint256"}],
                     "name": "CFXsUnlocked",
                     "type": "event"},
                    {"inputs": [], "name": "CFXsCounter", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                     "stateMutability": "view",
                     "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "name": "CFXss",
                                           "outputs": [{"internalType": "uint256", "name": "id", "type": "uint256"},
                                                       {"internalType": "address", "name": "owner", "type": "address"},
                                                       {"internalType": "uint256", "name": "amount", "type": "uint256"},
                                                       {"internalType": "string", "name": "data", "type": "string"}], "stateMutability": "view",
                                           "type": "function"},
                    {"inputs": [], "name": "CreateCFXs", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {
                        "inputs": [{"internalType": "uint256", "name": "CFXsId", "type": "uint256"},
                                   {"internalType": "address", "name": "_to", "type": "address"},
                                   {"internalType": "uint256", "name": "_amount", "type": "uint256"}], "name": "DangerTransfer", "outputs": [],
                        "stateMutability": "nonpayable", "type": "function"},
                    {"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "name": "LockedCFXs",
                     "outputs": [{"internalType": "uint256", "name": "_ether", "type": "uint256"},
                                 {"internalType": "uint256", "name": "locktime", "type": "uint256"}], "stateMutability": "view", "type": "function"},
                    {
                        "inputs": [{"internalType": "uint256", "name": "CFXsId", "type": "uint256"},
                                   {"internalType": "uint256", "name": "_ether", "type": "uint256"},
                                   {"internalType": "uint256", "name": "locktime", "type": "uint256"}], "name": "LockingScript", "outputs": [],
                        "stateMutability": "nonpayable", "type": "function"},
                    {"inputs": [{"internalType": "uint256", "name": "CFXsId", "type": "uint256"}], "name": "OwnerUnlockingScript", "outputs": [],
                     "stateMutability": "nonpayable", "type": "function"},
                    {"inputs": [{"internalType": "uint256", "name": "CFXsId", "type": "uint256"}], "name": "UnlockingScript", "outputs": [],
                     "stateMutability": "payable", "type": "function"},
                    {"inputs": [{"internalType": "address", "name": "_addr", "type": "address"}], "name": "balanceOf",
                     "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
                    {"inputs": [{"internalType": "uint256", "name": "_id", "type": "uint256"}], "name": "getLockStates",
                     "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
                    {"inputs": [{"internalType": "uint256", "name": "CFXsId", "type": "uint256"},
                                {"internalType": "string", "name": "_data", "type": "string"}],
                     "name": "inscribe", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"components": [
                {"internalType": "uint256[]", "name": "inputs", "type": "uint256[]"}, {
                    "components": [{"internalType": "address", "name": "owner", "type": "address"},
                                   {"internalType": "uint256", "name": "amount", "type": "uint256"},
                                   {"internalType": "string", "name": "data", "type": "string"}],
                    "internalType": "struct CFXsContract.OutputCFXsData[]",
                    "name": "outputs", "type": "tuple[]"}], "internalType": "struct CFXsContract.Transaction", "name": "_tx", "type": "tuple"}],
                        "name": "processTransaction", "outputs": [],
                        "stateMutability": "nonpayable",
                        "type": "function"},
                    {"inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                     "stateMutability": "view",
                     "type": "function"}, {"stateMutability": "payable", "type": "receive"}]
        # 获取代币合约实例
        contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi_json)
        # 获取代币余额
        balance = contract.functions.balanceOf(Web3.to_checksum_address(addr)).call()
        # 将余额转换为代币单位（以太为例，小数点18位）
        # decimals = contract.functions.decimals().call()
        # balance_in_units = balance / (10 ** decimals)
        print(f'【{addr}】【合约代币：{contract_address}】余额：{balance}')
        return balance

    def tranfer_token_by_abi(self, qw3, contract_address, to_address, val):
        """
        转任意代币(注意单位！！！)
        """
        # 合约 ABI
        abi = [
            {
                "inputs": [
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"}
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
        # 创建合约对象
        contract = qw3.eth.contract(address=contract_address, abi=abi)
        # 转账操作
        tx_hash = contract.functions.transfer(Web3.to_checksum_address(to_address), val).transact({'from': Web3.to_checksum_address(self.address)})
        # 等待交易确认
        tx_receipt = qw3.eth.waitForTransactionReceipt(tx_hash)
        print(f"Token【{contract_address}】转给【{to_address}】成功,数量: {val}， hash: {tx_hash}")

    def get_721_nfts(self, wb3, contract_address, addr=None):
        """
        获取某个账号上的NFT（包括元数据）
        """
        if not addr:
            addr = self.address
        contract_abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}, {"name": "_index", "type": "uint256"}],
                "name": "tokenOfOwnerByIndex",
                "outputs": [{"name": "tokenId", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [{"name": "_tokenId", "type": "uint256"}],
                "name": "tokenURI",
                "outputs": [{"name": "", "type": "string"}],
                "type": "function"
            }
            # ... 其他可能的合约方法 ...
        ]
        # 创建合约实例
        nft_contract = wb3.eth.contract(address=contract_address, abi=contract_abi)
        # 查询该地址拥有的 ERC-721 NFT 总数
        nft_count = nft_contract.functions.balanceOf(addr).call()
        # 查询每个 NFT 的 tokenId
        nft_metadata_list = []
        for i in range(nft_count):
            token_id = nft_contract.functions.tokenOfOwnerByIndex(addr, i).call()
            token_uri = nft_contract.functions.tokenURI(token_id).call()
            if "application/json" in str(token_uri):
                # 解码 Base64 编码的字符串为字节数据
                decoded_utf8 = base64.b64decode(token_uri.split('base64,')[1]).decode('utf-8')
                # 解析 UTF-8 字符串为 JSON 对象
                token_uri = json.loads(decoded_utf8)
            nft_metadata_list.append({"token_id": token_id, "token_uri": token_uri})
        print("NFT Metadata for", addr, ":", nft_metadata_list)
        return nft_metadata_list

    def save_balance_info(self, log_name="余额情况"):
        balance_info = ""
        chains_info = []
        for chain_name, web3_instance in self.chain_instances.items():
            balance_info = f"{balance_info}----【{chain_name}】余额----{self.get_balance_from_attr(chain_name)}"
            chains_info.append(f"{chain_name}余额:{self.get_balance_from_attr(chain_name)}")
        print(f"【{self.index}】【{self.address}】余额情况 {','.join(chains_info)}")
        QGEth.lock.acquire()
        with open(f"{log_name}.txt", 'a', encoding='utf-8') as f:
            f.write(
                f'{self.index}----{self.address}----{self.private_key}----{self.mnemonic if self.mnemonic else "无"}----{balance_info}\n')
            f.close()
        QGEth.lock.release()

    def sign_msg(self, w3, msg):
        # 消息签名
        message = encode_defunct(text=msg)
        signed_message = w3.eth.account.sign_message(message, private_key=self.private_key)
        signed_data = signed_message.signature
        # print("签名后:" + signed_data.hex())
        return signed_data.hex()

    def sign_msg_v2(self, msg):
        # 消息签名
        message = encode_defunct(text=msg)
        signed_message = w3.eth.account.sign_message(message, private_key=self.private_key)
        signed_data = signed_message.signature
        # print("签名后:" + signed_data.hex())
        return signed_data.hex()

    def sign_712(self, data):
        encoded_message = encode_structured_data(data)
        signed_message = Account.sign_message(encoded_message, private_key=self.private_key)
        # print('Signature:', signed_message.signature.hex())
        return signed_message.signature.hex()

    @retry(tries=5, delay=1, backoff=2, max_delay=5)
    def get_data(self, chain_name, req_type, *params):
        url = f"{QGEth.bases.get(chain_name)}{QGEth.apis.get(req_type).format(*params)}&page=1&offset=10000&sort=asc"
        resp = requests.Session().get(url)
        # print(resp.json())
        if "Too Many Requests" in resp.text or "Max rate limit reached, please use API Key for higher rate limit" in resp.text:
            raise Exception("重试！")
        return resp.json()['result']

    @classmethod
    def check_tx_found_in_txs(cls, txs, to_addr, search_data=None):
        """
        检查tx是否已存在
        :param txs: 某个链的交易纪录合集
        :param to_addr:
        :param search_data:
        :return:
        """
        if not txs:
            return []
        filter_txs = [obj for obj in txs if
                      obj.get('isError') == '0' and to_addr.lower() in str(obj.get('to')).lower() and obj.get(
                          'txreceipt_status') == '1']
        if search_data:
            filter_txs = [obj for obj in filter_txs if str(search_data).lower() in str(obj.get('input')).lower()]
        return filter_txs

    @staticmethod
    def get_current_gas_info(w3, tx):
        estimated_gas = w3.eth.estimate_gas(tx)
        gas_price = round(w3.from_wei(w3.eth.gas_price, "gwei"), 8)
        return estimated_gas, gas_price

    @staticmethod
    def assemble_tx_with_gas(w3, tx, gas_limit_offset=0.0, gas_price_offset=1.0, fee_eth=0.03):
        estimated_gas, gas_price = QGEth.get_current_gas_info(w3, tx)
        # gas limit偏移
        max_estimated_gas = estimated_gas + gas_limit_offset
        # gas price偏移
        max_fee_per_gas = gas_price + Decimal(gas_price_offset)
        max_priority_fee_per_gas = gas_price + Decimal(gas_price_offset - 0.001)
        # 计算预估手续费
        estimated_fee_eth = (Decimal(max_estimated_gas) * max_fee_per_gas) / 1000000000
        print(
            f"目标地址【{tx['to']}】:预估Gas:{estimated_gas},预估Gas Price:{gas_price}Gwei,预估手续费:{estimated_fee_eth}Eth")
        # if estimated_fee_eth > fee_eth:
        #     raise Exception(f"手续费：{estimated_fee_eth}过高！跳过！")
        gas_info = {
            "gas": estimated_gas,
            "maxFeePerGas": Web3.to_wei(max_fee_per_gas, "gwei"),  # 最大矿工费用
            'maxPriorityFeePerGas': Web3.to_wei(max_priority_fee_per_gas, 'gwei'),  # 最大优先矿工费用
        }
        tx.update(gas_info)
        return tx

    def send_tx(self, w3, tx, to_address, log_name, is_wait=True):
        """发送交易"""
        try:
            signed_txn = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
            # 发送交易
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            log_info(f"【{self.index}】【{self.address}】动作：{log_name},目标地址：{to_address},发送tx: {tx_hash.hex()}")
            if is_wait:
                # 等待交易确认
                tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60, poll_latency=5)
                log_info(f"【{self.index}】【{self.address}】动作：{log_name},目标地址：{to_address},发送成功！tx: {tx_receipt.transactionHash.hex()}")
                self.log(f'{log_name}-成功结果',
                         f'{self.address}----{self.private_key}----{to_address}----{tx_hash.hex()}\n')
            else:
                log_info(f"【{self.index}】【{self.address}】动作：{log_name},目标地址：{to_address},发送成功（仅发送）！tx: {tx_hash.hex()}")
            return tx_hash.hex()
        except Exception as e:
            log_info(f"【{self.index}】【{self.address}】动作：{log_name}执行失败,报文：{e}")
            self.log(f'{log_name}-失败结果', f'{self.address}----{self.private_key}----{to_address}----{e}\n')
            return None

    def sent_tx_with_assembled(self, w3, to_address, value, input_data, action_name, gas_limit_offset=0.0, gas_price_offset=0.1, fee_eth=0.03,
                               is_wait_tx=True):
        """
        组装参数并发送交易
        """
        nonce = w3.eth.get_transaction_count(Web3.to_checksum_address(self.address), 'pending')
        print(f'{self.address} nonce:{nonce}')
        tx = {
            'from': Web3.to_checksum_address(self.address),
            'to': Web3.to_checksum_address(to_address),
            'value': Web3.to_wei(value, 'ether'),
            'data': input_data.lower(),
            # 'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(self.address)),
            'nonce': nonce,
            'chainId': w3.eth.chain_id,
            'type': 2
        }
        try:
            self.assemble_tx_with_gas(w3, tx, gas_limit_offset=gas_limit_offset, gas_price_offset=gas_price_offset,
                                      fee_eth=fee_eth)
            tx_hash = self.send_tx(w3, tx, to_address, action_name, is_wait_tx)
            return tx_hash
        except Exception as e:
            print(f"【{self.index}】【{self.address}】动作【{action_name}】预估会失败，跳过！报文：{e}")
            return None

    def sent_tx_with_assembled_by_type0(self, w3, to_address, value, input_data, action_name, gas=None, gas_price=None, is_wait_tx=True):
        """
        组装参数并发送交易
        """
        try:
            nonce = w3.eth.get_transaction_count(Web3.to_checksum_address(self.address), 'pending')
            print(f'{self.address} nonce:{nonce}')
            tx = {
                'from': Web3.to_checksum_address(self.address),
                'to': Web3.to_checksum_address(to_address),
                'value': Web3.to_wei(value, 'ether'),
                # 'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(self.address)),
                'nonce': nonce,
                'chainId': w3.eth.chain_id,
            }
            if input_data:
                tx.update({"data": input_data.lower()})
            if gas and gas_price:
                tx.update({
                    "gas": gas,
                    'gasPrice': Web3.to_wei(gas_price, "gwei")
                })
            else:
                estimated_gas, gas_price = QGEth.get_current_gas_info(w3, tx)
                tx.update({
                    "gas": estimated_gas,
                    'gasPrice': Web3.to_wei(gas_price, "gwei")
                })
            print(tx)
            return self.send_tx(w3, tx, to_address, action_name, is_wait_tx)
        except Exception as e:
            print(f"【{self.index}】【{self.address}】动作【{action_name}】预估会失败，跳过！报文：{e}")

    def sent_with_full_tx(self, w3, to_address, value, input_data, gas, action_name):
        """
        组装完整tx并发送交易(不计算gas)
        """
        tx = {
            'from': Web3.to_checksum_address(self.address),
            'to': Web3.to_checksum_address(to_address),
            'value': Web3.to_wei(value, 'ether'),
            'data': input_data.lower(),
            'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(self.address)),
            'chainId': w3.eth.chain_id,
            "gas": gas,
            'gasPrice': Web3.to_wei("1", "gwei"),
            # "maxFeePerGas": Web3.to_wei("1.000000019", "gwei"),  # 最大矿工费用
            # 'maxPriorityFeePerGas': Web3.to_wei("1", "gwei"),  # 最大优先矿工费用
            'type': 0
        }
        try:
            self.send_tx(w3, tx, to_address, action_name)
        except Exception as e:
            print(f"【{self.index}】【{self.address}】动作【{action_name}】预估会失败，跳过！报文：{e}")

    @staticmethod
    def decode_param(input_data):
        if len(input_data) < 10:
            print("全空调用")
            return
        method_id = input_data[:10]
        remaining = input_data[10:]
        params_hex = [remaining[i:i + 64] for i in range(0, len(remaining), 64)]
        index = 0
        print(f"函数方法:{method_id}")
        for param_hex in params_hex:
            if param_hex[:7] == '0000000' and param_hex[-7:] == "0000000":
                print(f"参数{index},占位类型:{param_hex}")
            elif param_hex[:7] == '0000000' and param_hex[-7:] != "0000000" and param_hex[24:28] == '0000':
                print(f"参数{index},数字类型: 解码后:{int(param_hex, 16)},原码: {param_hex}")
            elif param_hex[:7] == '0000000' and param_hex[-7:] != "0000000" and param_hex[24:28] != '0000':
                print(f"参数{index},地址类型: 解码后：0x{param_hex[24:]},原码: {param_hex}")
            elif param_hex[:7] != '0000000':
                try:
                    byteStr = bytes.fromhex(param_hex)
                    decode_str = byteStr.decode('utf-8')
                    # decode_str = byteStr.decode('Latin-1')
                except Exception as e:
                    decode_str = param_hex
                print(f"参数{index},字符类型:解码后:{decode_str},原码: {param_hex}")
            else:
                print(f"空类型参！{param_hex}")
            index = index + 1

        print(f"{'==' * 50}")

    @staticmethod
    def extract_parameters(input_data):
        def decode_param_value(param_value):
            # 如果参数值长度超过 40 位，则认为是 uint256
            if '0' * 40 in param_value:
                return int(param_value, 16)
            else:
                return Web3.to_checksum_address("0x" + param_value[24:])

        # 函数选择器长度（4 字节）
        function_selector_length = 10

        # 参数值的长度（32 字节）
        param_length = 64

        # 从inputdata中提取函数选择器
        function_selector = input_data[:function_selector_length]

        # 从inputdata中提取参数部分
        params_data = input_data[function_selector_length:]

        # 参数列表
        params = []

        # 逐步提取参数值
        while params_data:
            if len(params_data) < param_length:
                break
            param_value = params_data[:param_length]
            decoded_value = decode_param_value(param_value)
            params.append(decoded_value)

            # 剩余参数
            params_data = params_data[param_length:]

        print("函数选择器：", function_selector)
        print("参数值列表：", params)
        return function_selector, params

    @staticmethod
    def log(log_name, info):
        # 获取调用方的文件路径
        caller_file = inspect.stack()[-1].filename
        # 构建 logs 目录的完整路径
        logs_dir = Path(caller_file).resolve().parent / 'logs'
        # 确保 logs 目录存在
        logs_dir.mkdir(parents=True, exist_ok=True)
        with open(f"{logs_dir}/{log_name}.txt", 'a', encoding='utf-8') as f:
            f.write(f'{info}')
            f.close()

    def random_str(self, length):
        """指定长度的随机字符"""
        str = "abcdefghijklmnopqrstuvwxyz"
        return "".join(random.choice(str) for i in range(length))


if __name__ == '__main__':
    p1 = "0x624f82f5000000000000000000000000000000000000000000000000000000000000014600000000000000000000000000000000000000000000000000000000003826ac000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000412a2d1d4a13795bacd46f9abf8aaa1894453444a0018d83a437f0a6f35bf107b414668b591213b71f38b07cc135d34413c1442657652fd20c2cab84df92bb9d091c00000000000000000000000000000000000000000000000000000000000000"
    p2 = "0xb341ee9f000000000000000000000000000000000000000000000000000000000000423100000000000000000000000000000000000000000000000000002eb6bdd7a374000000000000000000000000000000000000000000000000000000000000012c"

    p3 = "0xb341ee9f000000000000000000000000000000000000000000000000000000000000161000000000000000000000000000000000000000000000000000000f92030f88150000000000000000000000000000000000000000000000000000000000000064"
    p4 = "0xb341ee9f000000000000000000000000000000000000000000000000000000000000dca100000000000000000000000000000000000000000000000000009bac1409389500000000000000000000000000000000000000000000000000000000000003ea"
    QGEth.decode_param(p1)
    QGEth.decode_param(p2)
    QGEth.decode_param(p3)
    QGEth.decode_param(p4)
    # time1 = (datetime.utcnow() + timedelta(hours=8, minutes=5)).timestamp()
    # timestamp = hex(int(time1))[2:].rjust(64, '0')
    # print(time1,timestamp)
    # hex_string = "0x53f4fd5c293f9def2d949ad6b282ad348967195adc0c7c23e3fdf11c193f57e0"
    #
    # # 去掉前缀 "0x" 后再处理
    # clean_hex_string = hex_string[2:] if hex_string.startswith("0x") else hex_string
    # result_string = bytes.fromhex(clean_hex_string).decode('utf-8', 'ignore')
    # print(result_string)
