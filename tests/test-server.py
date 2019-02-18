#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
from srrpy import Server
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

name = "test"
db = redis.Redis()
codec = "json"
test_server = Server(db,name,5,codec)
test_server.run()

