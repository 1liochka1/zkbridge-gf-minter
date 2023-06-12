import json
import time
from web3 import Web3
import requests
from fake_useragent import UserAgent
from loguru import logger
from eth_account.messages import encode_defunct
from tqdm import tqdm
import random
from web3.middleware import geth_poa_middleware
from moralis import evm_api
from config import *
import pandas as pd

zk_abi = '[{"inputs":[{"internalType":"uint256","name":"_mintStartTime","type":"uint256"},{"internalType":"uint256","name":"_mintEndTime","type":"uint256"},{"internalType":"uint256","name":"_mintLimit","type":"uint256"},{"internalType":"string","name":"_metadataUri","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ApprovalCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"ApprovalQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"BalanceQueryForZeroAddress","type":"error"},{"inputs":[],"name":"InvalidQueryRange","type":"error"},{"inputs":[],"name":"MintERC2309QuantityExceedsLimit","type":"error"},{"inputs":[],"name":"MintToZeroAddress","type":"error"},{"inputs":[],"name":"MintZeroQuantity","type":"error"},{"inputs":[],"name":"OwnerQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"OwnershipNotInitializedForExtraData","type":"error"},{"inputs":[],"name":"TransferCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"TransferFromIncorrectOwner","type":"error"},{"inputs":[],"name":"TransferToNonERC721ReceiverImplementer","type":"error"},{"inputs":[],"name":"TransferToZeroAddress","type":"error"},{"inputs":[],"name":"URIQueryForNonexistentToken","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"fromTokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"toTokenId","type":"uint256"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"ConsecutiveTransfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"explicitOwnershipOf","outputs":[{"components":[{"internalType":"address","name":"addr","type":"address"},{"internalType":"uint64","name":"startTimestamp","type":"uint64"},{"internalType":"bool","name":"burned","type":"bool"},{"internalType":"uint24","name":"extraData","type":"uint24"}],"internalType":"struct IERC721A.TokenOwnership","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"name":"explicitOwnershipsOf","outputs":[{"components":[{"internalType":"address","name":"addr","type":"address"},{"internalType":"uint64","name":"startTimestamp","type":"uint64"},{"internalType":"bool","name":"burned","type":"bool"},{"internalType":"uint24","name":"extraData","type":"uint24"}],"internalType":"struct IERC721A.TokenOwnership[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"userAddress","type":"address"}],"name":"getMintSurplus","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"mintEndTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"mintLimit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"mintStartTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_newMetadataUri","type":"string"}],"name":"setMetadataUri","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_mintLimit","type":"uint256"}],"name":"setMintLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_mintStartTime","type":"uint256"},{"internalType":"uint256","name":"_mintEndTime","type":"uint256"}],"name":"setMintTimes","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"tokensOfOwner","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"start","type":"uint256"},{"internalType":"uint256","name":"stop","type":"uint256"}],"name":"tokensOfOwnerIn","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
bridge_abi = '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"beacon","type":"address"}],"name":"BeaconUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"oldContract","type":"address"},{"indexed":true,"internalType":"address","name":"newContract","type":"address"}],"name":"ContractUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"pendingImplementation","type":"address"},{"indexed":true,"internalType":"address","name":"newImplementation","type":"address"}],"name":"NewPendingImplementation","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint64","name":"sequence","type":"uint64"},{"indexed":false,"internalType":"address","name":"sourceToken","type":"address"},{"indexed":false,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokenID","type":"uint256"},{"indexed":false,"internalType":"uint16","name":"sourceChain","type":"uint16"},{"indexed":false,"internalType":"uint16","name":"sendChain","type":"uint16"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"}],"name":"ReceiveNFT","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"chainId","type":"uint16"},{"indexed":false,"internalType":"address","name":"nftBridge","type":"address"}],"name":"RegisterChain","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint64","name":"sequence","type":"uint64"},{"indexed":false,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokenID","type":"uint256"},{"indexed":false,"internalType":"uint16","name":"recipientChain","type":"uint16"},{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"}],"name":"TransferNFT","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"inputs":[],"name":"MIN_LOCK_TIME","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"chainId_","type":"uint16"}],"name":"bridgeContracts","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"chainId","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"confirmContractUpgrade","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"destChainId","type":"uint16"}],"name":"fee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"impl","type":"address"}],"name":"isInitialized","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"isWrappedAsset","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lockTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC721Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingImplementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"chainId","type":"uint16"},{"internalType":"address","name":"contractAddress","type":"address"}],"name":"registerChain","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"destChainId","type":"uint16"},{"internalType":"uint256","name":"fee","type":"uint256"}],"name":"setFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"lockTime","type":"uint256"}],"name":"setLockTime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"zkBridge","type":"address"}],"name":"setZkBridge","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"submitContractUpgrade","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"toUpdateTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"tokenImplementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"tokenID","type":"uint256"},{"internalType":"uint16","name":"recipientChain","type":"uint16"},{"internalType":"bytes32","name":"recipient","type":"bytes32"}],"name":"transferNFT","outputs":[{"internalType":"uint64","name":"sequence","type":"uint64"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint16","name":"tokenChainId","type":"uint16"},{"internalType":"bytes32","name":"tokenAddress","type":"bytes32"}],"name":"wrappedAsset","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"zkBridge","outputs":[{"internalType":"contract IZKBridge","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"srcChainId","type":"uint16"},{"internalType":"address","name":"srcAddress","type":"address"},{"internalType":"uint64","name":"sequence","type":"uint64"},{"internalType":"bytes","name":"payload","type":"bytes"}],"name":"zkReceive","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
zk_polygon_abi = '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"beacon","type":"address"}],"name":"BeaconUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"oldContract","type":"address"},{"indexed":true,"internalType":"address","name":"newContract","type":"address"}],"name":"ContractUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":true,"internalType":"uint16","name":"srcChainId","type":"uint16"},{"indexed":true,"internalType":"uint64","name":"sequence","type":"uint64"},{"indexed":false,"internalType":"address","name":"dstAddress","type":"address"},{"indexed":false,"internalType":"bytes","name":"payload","type":"bytes"}],"name":"ExecutedMessage","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":true,"internalType":"uint16","name":"dstChainId","type":"uint16"},{"indexed":true,"internalType":"uint64","name":"sequence","type":"uint64"},{"indexed":false,"internalType":"address","name":"dstAddress","type":"address"},{"indexed":false,"internalType":"bytes","name":"payload","type":"bytes"}],"name":"MessagePublished","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"pendingImplementation","type":"address"},{"indexed":true,"internalType":"address","name":"newImplementation","type":"address"}],"name":"NewPendingImplementation","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"MESSAGE_TOPIC","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MIN_LOCK_TIME","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"chainId","type":"uint16"}],"name":"blockUpdater","outputs":[{"internalType":"contract IBlockUpdater","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"chainId","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimFees","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"confirmContractUpgrade","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"impl","type":"address"}],"name":"isInitialized","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"hash","type":"bytes32"}],"name":"isTransferCompleted","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lockTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"chainId","type":"uint16"}],"name":"mptVerifier","outputs":[{"internalType":"contract IMptVerifier","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"hash","type":"bytes32"}],"name":"nextSequence","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingImplementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"chainId","type":"uint16"},{"internalType":"bytes32","name":"bridgeContract","type":"bytes32"}],"name":"registerChain","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"address","name":"dstAddress","type":"address"},{"internalType":"bytes","name":"payload","type":"bytes"}],"name":"send","outputs":[{"internalType":"uint64","name":"sequence","type":"uint64"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint16","name":"chainId","type":"uint16"},{"internalType":"address","name":"blockUpdater","type":"address"}],"name":"setBlockUpdater","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"lockTime","type":"uint256"}],"name":"setLockTime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"chainId","type":"uint16"},{"internalType":"address","name":"mptVerifier","type":"address"}],"name":"setMptVerifier","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"submitContractUpgrade","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"toUpdateTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"srcChainId","type":"uint16"},{"internalType":"bytes32","name":"srcBlockHash","type":"bytes32"},{"internalType":"uint256","name":"logIndex","type":"uint256"},{"internalType":"bytes","name":"mptProof","type":"bytes"}],"name":"validateTransactionProof","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"chainId","type":"uint16"}],"name":"zkBridgeContracts","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]'


rpc = {'1':'https://rpc.ankr.com/bsc',
       '0':'https://bsc.publicnode.com',
       'bsc':'https://bsc.publicnode.com'}


chainId = {'bsc':3,
           'polygon':4}


id = {'bsc':56,
    'polygon':137}

scans = {'bsc':'https://bscscan.com/tx/',
         'polygon':'https://polygonscan.com/tx/'}
class Help:
    def check_status_tx(self,tx_hash,):
        logger.info(f'{self.address} - жду подтверждения транзакции...')

        while True:
            try:
                status = self.w3.eth.get_transaction_receipt(tx_hash)['status']
                if status in [0, 1]:
                    return status
                time.sleep(1)
            except Exception as error:
                time.sleep(1)

    def sleep_indicator(self, sec):
        for i in tqdm(range(sec), desc='жду', bar_format="{desc}: {n_fmt}c /{total_fmt}c {bar}", colour='green'):
            time.sleep(1)

class ZkBridge(Help):
    def __init__(self,privatekey,delay,chain,to, mode, api,proxy=None):
        self.privatekey = privatekey
        self.chain = chain
        self.to = to
        self.w3 = Web3(Web3.HTTPProvider(rpc[chain]))
        self.account = self.w3.eth.account.from_key(self.privatekey)
        self.address = self.account.address
        self.mode = str(mode)
        self.delay = delay
        self.proxy = proxy
        self.moralisapi = api

    def auth(self):
        ua = UserAgent()
        ua = ua.random
        headers = {
            'authority': 'api.zkbridge.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://zkbridge.com',
            'referer': 'https://zkbridge.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': ua,
        }

        json_data = {
            'publicKey': self.address.lower(),
        }

      
        while True:
            try:
                if self.proxy:
                    proxies = {'http': self.proxy, 'https': self.proxy}
                    response = requests.post(
                        'https://api.zkbridge.com/api/signin/validation_message',
                        json=json_data, headers=headers, proxies=proxies
                    )
                else:
                    response = requests.post(
                        'https://api.zkbridge.com/api/signin/validation_message',
                        json=json_data, headers=headers,

                    )

                if response.status_code == 200:
                    msg = json.loads(response.text)

                    msg = msg['message']
                    msg = encode_defunct(text=msg)
                    sign = self.w3.eth.account.sign_message(msg, private_key=self.privatekey)
                    signature = self.w3.to_hex(sign.signature)
                    json_data = {
                        'publicKey': self.address,
                        'signedMessage': signature,
                    }
                    
                    return signature, ua
            except Exception as e:
                logger.error(f'{self.address}:{self.chain} - {e}')
                time.sleep(5)

    def sign(self):

        # sign msg
        signature, ua = self.auth()
        headers = {
            'authority': 'api.zkbridge.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://zkbridge.com',
            'referer': 'https://zkbridge.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': ua,
        }

        json_data = {
            'publicKey': self.address.lower(),
            'signedMessage': signature,
        }
       
        while True:
            try:

                if self.proxy:
                    proxies = {'http': self.proxy, 'https': self.proxy}

                    response = requests.post('https://api.zkbridge.com/api/signin', headers=headers, json=json_data,
                                             proxies=proxies)
                else:
                    response = requests.post('https://api.zkbridge.com/api/signin', headers=headers, json=json_data)
                
                if response.status_code == 200:
                    token = json.loads(response.text)['token']
                    headers['authorization'] = f'Bearer {token}'
                    session = requests.session()
                    session.headers.update(headers)
                    return session

            except Exception as e:
                logger.error(F'{self.address}:{self.chain} - {e}')
                time.sleep(5)

    def profile(self):
        session = self.sign()
        params = ''
        try:
            if self.proxy:
                proxies = {'http': self.proxy, 'https': self.proxy}
                response = session.get('https://api.zkbridge.com/api/user/profile', params=params,proxies=proxies)
            else:
                response = session.get('https://api.zkbridge.com/api/user/profile', params=params)
            if response.status_code == 200:
                logger.success(f'{self.address}:{self.chain} - успешно авторизовался...')
                return session
        except Exception as e:
            logger.error(f'{self.address}:{self.chain} - {e}')
            return False

    def balance_and_get_id(self):
        try:
            api_key = self.moralisapi
            params = {
                "chain": self.chain,
                "format": "decimal",
                "token_addresses": [
                    '0x13D23d867e73aF912Adf5d5bd47915261eFa28F2'
                ],
                "media_items": False,
                "address": self.address}

            result = evm_api.nft.get_wallet_nfts(api_key=api_key,params=params)
            id_ = int(result['result'][0]['token_id'])
            if id_:
                logger.success(f'{self.address}:{self.chain} - успешно найдена greenfield {id_}...')
                return id_


        except Exception as e:
            if 'list index out of range' in str(e):
                logger.error(f'{self.address}:{self.chain} - на кошельке отсутсвует greenfield нфт...')
                return None
            else:
                logger.error(f'{self.address}:{self.chain} - {e}...')


    def mint(self):
        while True:
            self.w3 = Web3(Web3.HTTPProvider(rpc[self.mode]))
            greenfield = self.w3.eth.contract(address=Web3.to_checksum_address('0x13D23d867e73aF912Adf5d5bd47915261eFa28F2'), abi=zk_abi)
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

            session = self.profile()
            if not session:
                return False
            try:
                if session:
                    tx = greenfield.functions.mint().build_transaction({
                        'from': self.address,
                        'gas': greenfield.functions.mint().estimate_gas({'from':self.address,'nonce': self.w3.eth.get_transaction_count(self.address), }),
                        'nonce': self.w3.eth.get_transaction_count(self.address),
                        'gasPrice': self.w3.eth.gas_price
                    })

                    if self.mode == 0:
                        tx['gasPrice'] = self.w3.eth.gas_price
                    else:
                        tx['gasPrice'] = int(1.5*10**9)
                    logger.info(f'{self.address}:{self.chain} - начинаю минт...')
                    sign = self.account.sign_transaction(tx)
                    hash = self.w3.eth.send_raw_transaction(sign.rawTransaction)
                    status = self.check_status_tx(hash)
                    self.sleep_indicator(5)
                    if status == 1:
                        logger.success(f'{self.address}:{self.chain} - успешно заминтил : {scans[self.chain]}{self.w3.to_hex(hash)}...')
                        self.sleep_indicator(random.randint(self.delay[0], self.delay[1]))                    # delay
                        return session
            except Exception as e:
                error = str(e)
                if 'INTERNAL_ERROR: insufficient funds' in error or 'insufficient funds for gas * price + value' in error:
                    logger.error(
                        f'{self.address}:{self.chain} - не хватает денег на газ, заканчиваю работу через 5 секунд...')
                    time.sleep(5)
                    break
                else:
                    logger.error(f'{self.address}:{self.chain} - {e}...')
                    return False

    def bridge(self):
        if self.chain == 'bsc':
            rpc_ = rpc[self.mode]
            self.w3 = Web3(Web3.HTTPProvider(rpc_))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)


        session = self.mint()
        id_ = self.balance_and_get_id()
        greenfield = self.w3.eth.contract(address=Web3.to_checksum_address('0x13D23d867e73aF912Adf5d5bd47915261eFa28F2'),abi=zk_abi)

        #appoove
        while True:
            if id_:
                try:
                    tx = greenfield.functions.approve(Web3.to_checksum_address('0xE09828f0DA805523878Be66EA2a70240d312001e'),id_).build_transaction({
                        'from': self.address,
                        'gas': greenfield.functions.approve(Web3.to_checksum_address('0xE09828f0DA805523878Be66EA2a70240d312001e'),id_).estimate_gas({'from':self.address,'nonce': self.w3.eth.get_transaction_count(self.address)}),
                        'nonce': self.w3.eth.get_transaction_count(self.address),
                        'gasPrice': self.w3.eth.gas_price

                    })

                    if self.mode == 0:
                        tx['gasPrice'] = self.w3.eth.gas_price
                    else:
                        tx['gasPrice'] = int(1.5 * 10 ** 9)
                    logger.info(f'{self.address}:{self.chain} - начинаю апрув greenfield {id_}...')
                    sign = self.account.sign_transaction(tx)
                    hash = self.w3.eth.send_raw_transaction(sign.rawTransaction)
                    status = self.check_status_tx(hash)
                    self.sleep_indicator(5)
                    if status == 1:
                        logger.success(f'{self.address}:{self.chain} - успешно апрувнул greenfield {id_} : {scans[self.chain]}{self.w3.to_hex(hash)}...')
                        self.sleep_indicator(random.randint(1,10))
                        break
                except Exception as e:
                    error = str(e)
                    if 'INTERNAL_ERROR: insufficient funds' in error or 'insufficient funds for gas * price + value' in error:
                        logger.error(
                            f'{self.address}:{self.chain} - не хватает денег на газ, заканчиваю работу через 5 секунд...')
                        time.sleep(5)
                    else:
                        logger.error(f'{self.address}:{self.chain} - {e}...')
                        time.sleep(2)

        #bridge

        bridge = self.w3.eth.contract(address=Web3.to_checksum_address('0xE09828f0DA805523878Be66EA2a70240d312001e'),abi = bridge_abi)

        to = chainId[self.to]
        fee = bridge.functions.fee(to).call()
        logger.info(f'{self.address}:{self.chain} - начинаю бридж greenfield {id_}...')
        while True:
            try:
                enco = f'0x000000000000000000000000{self.address[2:]}'
                tx = bridge.functions.transferNFT(Web3.to_checksum_address('0x13D23d867e73aF912Adf5d5bd47915261eFa28F2'),id_, to, enco).build_transaction({
                    'from': self.address,
                    'value': fee,
                    'gas': bridge.functions.transferNFT(Web3.to_checksum_address('0x13D23d867e73aF912Adf5d5bd47915261eFa28F2'),id_, to, enco).estimate_gas(
                        {'from': self.address, 'nonce': self.w3.eth.get_transaction_count(self.address),'value':fee}),
                    'nonce': self.w3.eth.get_transaction_count(self.address),
                    'gasPrice': self.w3.eth.gas_price
                })
                if self.mode == 0:
                    tx['gasPrice'] = self.w3.eth.gas_price
                else:
                    tx['gasPrice'] = int(1.5 * 10 ** 9)
                sign = self.account.sign_transaction(tx)
                hash = self.w3.eth.send_raw_transaction(sign.rawTransaction)
                status = self.check_status_tx(hash)
                self.sleep_indicator(5)
                if status == 1:
                    logger.success(f'{self.address}:{self.chain} - успешно бриджанул greenfield {id_} : {scans[self.chain]}{self.w3.to_hex(hash)}...')
                    self.sleep_indicator(random.randint(1, 20))
                    return self.w3.to_hex(hash),session
            except Exception as e:
                error = str(e)
                if 'INTERNAL_ERROR: insufficient funds' in error or 'insufficient funds for gas * price + value' in error:
                    logger.error(f'{self.address}:{self.chain} - не хватает денег на газ, заканчиваю работу через 5 секунд...')
                    time.sleep(5)
                    break
                else:
                    logger.error(f'{self.address}:{self.chain} - {e}')
                    time.sleep(5)

    def getProofGenTime(self):
        data = self.bridge()
        if data:
            hash, session = data
        else:
            return False

        params = {
            'appid': chainId[self.chain],
            'txhash': hash,
            'testnet': 'false',
        }


        while True:
            try:
                if self.proxy:
                    proxies = {'http': self.proxy, 'https': self.proxy}
                    response = session.get('https://api.zkbridge.com/api/bridge/getProofGenerationTime',params=params,proxies=proxies)
                else:
                    response = session.get('https://api.zkbridge.com/api/bridge/getProofGenerationTime', params=params)
                if response.status_code == 200:
                    return session, hash
            except Exception as e:
                logger.error(f'{self.address}:{self.chain}- {e}')
                time.sleep(5)

    def create_order(self):
        nft_id = self.balance_and_get_id()
        data = self.getProofGenTime()
        if data:
            session, hash = data
        else:
            return False
        json_data = {
            'from': self.address,
            'to': self.address,
            'sourceChainId': id[self.chain] ,
            'targetChainId':id[self.to] ,
            'txHash': hash,
            'contracts': [
                {
                    'contractAddress': '0x13d23d867e73af912adf5d5bd47915261efa28f2',
                    'tokenId': nft_id,
                },
            ],
        }

        while True:
            try:
                if self.proxy:
                    proxies = {'http': self.proxy, 'https': self.proxy}
                    response = session.post('https://api.zkbridge.com/api/bridge/createOrder', json=json_data, proxies=proxies)
                else:
                    response = session.post('https://api.zkbridge.com/api/bridge/createOrder', json=json_data)
                if response.status_code == 200:
                    id_ = json.loads(response.text)['id']
                    logger.success(f'{self.address} - сгенерирован createOrder...')
                    return id_,session,hash
            except Exception as e:
                logger.error(f'{self.address}:{self.chain}- {e}')
                time.sleep(5)

    def gen_blob(self):
        data = self.create_order()
        if data:
            id_, session, hash = data
        else:
            return False
        json_data = {
            'tx_hash': hash,
            'chain_id': chainId[self.chain],
            'testnet': False,
        }
        while True:
            try:
                if self.proxy:
                    proxies = {'http': self.proxy, 'https': self.proxy}
                    response = session.post('https://api.zkbridge.com/api/v2/receipt_proof/generate', json=json_data, proxies=proxies)
                else:
                    response = session.post('https://api.zkbridge.com/api/v2/receipt_proof/generate', json=json_data)
                if response.status_code == 200:
                    data_ = json.loads(response.text)
                    self.sleep_indicator(random.randint(30,60))
                    logger.success(f'{self.address} - сгенерирован blob...')
                    return data_,id_,session

            except Exception as e:
                logger.error(f'{self.address}:{self.to}- {e}')
                time.sleep(5)

    def claimOrder(self,session,id,hash):
        json_data = {
            'claimHash': hash,
            'id': id,
        }

        while True:
            try:
                if self.proxy:
                    proxies = {'http': self.proxy, 'https': self.proxy}
                    response = session.post('https://api.zkbridge.com/api/bridge/claimOrder', json=json_data,proxies=proxies)
                else:
                    response = session.post('https://api.zkbridge.com/api/bridge/claimOrder', json=json_data)
                if response.status_code == 200:
                    logger.success(f'{self.address} - успешно забриджено!...')
                    self.sleep_indicator(random.randint(self.delay[0], self.delay[1]))
                    return True

            except Exception as e:
                logger.error(f'{self.address}:{self.to}- {e}')
                time.sleep(5)

    def check_status_tx2(self,w3,tx_hash,):
        logger.info(f'{self.address} - жду подтверждения транзакции...')

        while True:
            try:
                status = w3.eth.get_transaction_receipt(tx_hash)['status']
                if status in [0, 1]:
                    return status
                time.sleep(1)
            except Exception as error:
                time.sleep(1)

    def claim_on_destinaton(self):
        if self.mode == '1':
            logger.info(f'начинаю работу в режиме лоугаза с помощью ankrpc...')
        else:
            logger.info(f'начинаю работу в обычном режиме...')

        w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
        account = w3.eth.account.from_key(self.privatekey)
        address = account.address
        claim = w3.eth.contract(address=Web3.to_checksum_address('0xa25bE50be65070c2Ad96d5eD639061de31c45e12'),abi=zk_polygon_abi)
        data_, id_, session = self.gen_blob()
        while True:
            chainid = data_['chain_id']
            proof = data_['proof_index']
            blob = data_['proof_blob']
            block_hash = data_['block_hash']
            try:
                tx = claim.functions.validateTransactionProof(chainid,block_hash,proof,blob).build_transaction({
                    'from': address,
                    'gas': claim.functions.validateTransactionProof(chainid,block_hash,proof,blob).estimate_gas(
                        {'from': address, 'nonce': w3.eth.get_transaction_count(address)}),
                    'nonce': w3.eth.get_transaction_count(address),
                    'gasPrice': w3.eth.gas_price
                })
                sign = account.sign_transaction(tx)
                hash =w3.eth.send_raw_transaction(sign.rawTransaction)
                status = self.check_status_tx2(w3,hash)
                self.sleep_indicator(10)
                if status == 1:
                    logger.success(f'{address}:{self.to} - успешно заклеймил greenfield : {scans[self.to]}{w3.to_hex(hash)}...')
                    self.sleep_indicator(random.randint(1, 20))                #delay
                    order = self.claimOrder(session, id_, block_hash)
                    if order:
                        return address, 'success'
                    else:
                        return address, 'error'
            except Exception as e:
                error = str(e)
                if 'INTERNAL_ERROR: insufficient funds' in error or 'insufficient funds for gas * price + value' in error:
                    logger.error(f'{self.address}:{self.chain} - не хватает денег на газ, заканчиваю работу через 5 секунд...')
                    time.sleep(5)
                    return address, 'error'
                elif 'Message already executed' in error:
                    logger.success(f'{self.address}:{self.chain} - успешно заклеймил greenfield...')
                    return address, 'success'
                else:
                    logger.error(f'{address}:{self.to} - {e} ...')
                    return address, 'error'

def main():
    print(f'\n{" "*32}автор - https://t.me/iliocka{" "*32}\n')
    wallets, results =[], []
    chain = 'bsc'
    to = 'polygon'
    for key in keys:
        if proxies:
            proxy = random.choice(proxies)
        else:
            proxy = None
        mint = ZkBridge(key,DELAY,chain,to,MODE,MORALIS_API_KEY,proxy)
        res = mint.claim_on_destinaton()
        wallets.append(res[0]), results.append(res[1])
    res = {'address': wallets, 'result': results}
    df = pd.DataFrame(res)
    df.to_csv('results.csv', index=False)
    logger.success('Минетинг закончен...')

if __name__ == '__main__':
    main()
