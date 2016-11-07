#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging.config
import os
import json


def setup_logging(
        default_path='logging.json',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """ Setup logging configuration. """
    # see https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


setup_logging()
