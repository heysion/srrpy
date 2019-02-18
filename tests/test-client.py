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
'''

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class MyTemplate(TemplatesInterface):
    name = "mytemplate"
    metadata = __meta__data__

name = "test"
db = redis.Redis()
codec = "json"
tp = MyTemplate()
test_client = Client(db,name,5,codec,tp)
test_client.call(import_modules=["sys","os"],list_args={("a",10),("b",3)})
print(test_client.wait_result())

