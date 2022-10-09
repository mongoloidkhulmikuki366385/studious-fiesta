# -*- coding: utf-8 -*-
__author__ = 'Simon Liu'

import json


class GetConfig(object):
    def __init__(self, filepath=None):
        self.filepath = filepath
        self.config = None

    def get_config_information(self, config_key):
        if self.filepath:
            f = open(self.filepath, "rU")
            self.config = json.load(f)
            f.close()
            if isinstance(self.config, dict):
                return self.config.get(config_key)
            else:
                return 'config_dir ERROR or config_key ERROR'
        else:
            return 'pls make sure there are configs!'

