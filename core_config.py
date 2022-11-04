# -*- coding: utf-8 -*-

import json

class Settings:
    # logger conf file path
    LOGGER_CONF_PATH = "./logger_conf.json"
    LOGGER_CONF = None

_settings = Settings()
with open(_settings.LOGGER_CONF_PATH, 'r') as f:
    logger_conf = json.load(f)
_settings.LOGGER_CONF = logger_conf
settings = _settings
