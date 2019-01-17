#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
from templates import TemplatesInterface as testtf
from srr import Client
name = "test"
db = redis.Redis()
codec = "json"
tp = testtf()
test_client = Client(db,name,5,codec,tp)
test_client.call()
print(test_client.wait_result())

