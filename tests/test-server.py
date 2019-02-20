#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
from srrpy import Server
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

db = redis.Redis()

test_server = Server(db,queue="test",timeout=5,codec="json")

test_server.run()

