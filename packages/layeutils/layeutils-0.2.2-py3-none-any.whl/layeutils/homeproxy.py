from loguru import logger
import os

def using_home_server_proxy():
    logger.info('seting proxy...')
    proxy = 'socks5://192.168.1.81:7891'

    os.environ['http_proxy'] = proxy
    os.environ['https_proxy'] = proxy