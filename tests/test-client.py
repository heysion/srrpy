#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
from srrpy import TemplatesInterface
from srrpy import Client
import logging
import sys

__meta__data__ = '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

{% for mod in import_modules %}
import {{ mod }}
{% endfor %}

def run_test(a,b):
    print("a + b = %d"%(a+b))

run_test({% for item in list_args -%} {{ item[0] }} = {{ item[1] }} {%- if loop.index == list_args|length -%} {%- else %} , {% endif %} {%- endfor %})
time.sleep(5)
print("end")
'''

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class MyTemplate(TemplatesInterface):
    name = "mytemplate"
    metadata = __meta__data__

db = redis.Redis()

test_client = Client(db,queue="test",timeout=5,codec="json",templates=MyTemplate())

test_client.call(import_modules=["sys","os"],list_args={("a",10),("b",3)},execute="exec")

print(test_client.wait_result())

