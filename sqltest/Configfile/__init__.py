# -*- coding: utf-8 -*-
__author__ = 'Simon Liu'
import os
from getconfig import GetConfig


pwd = os.path.dirname(__file__)
config_dir = os.path.join(pwd, 'config.json')

MYSQL_CONFIG = GetConfig(config_dir).get_config_information('mysql_config')
HOST = MYSQL_CONFIG["host"]
USER = MYSQL_CONFIG["user"]
PASSWORD = MYSQL_CONFIG["password"]
DB = MYSQL_CONFIG["db"]
PORT = MYSQL_CONFIG["port"]
CHARSET = MYSQL_CONFIG["charset"]

