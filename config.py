import json
import os
from exception import ConfigException

class Config:
    def __init__(self, cfg_file):
        self.cfg_file = cfg_file
        f = open(cfg_file, 'r+', encoding='utf-8')
        tmp = json.loads(f.read())
        
        self.login_method   = tmp.get('login_method', '')
        self.token          = tmp.get('token', '')
        self.username       = tmp.get('username', '')
        self.password       = tmp.get('password', '')
        self.pid_dir        = tmp.get('pid_dir', '')
        self.command_prefix = tmp.get('command_prefix', '')

        if not self.login_method:
            raise ConfigException('Missing required config value: login_method')

        if not self.token and self.login_method == 'token':
            raise ConfigException('Missing required field token, no token was supplied for token login method')
        
        if (not self.username or not self.password) and self.login_method == 'account':
            raise ConfigException('No username or password were supplied for account login method')

        if not self.command_prefix:
            raise ConfigException('Missing required config value: command_prefix')
            
