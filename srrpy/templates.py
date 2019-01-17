#!/usr/bin/env python3
# -*- coding: utf-8 -*-
meta_data = '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

{% for mod in import_modules %}
import {{ mod }}
{% endfor %}

def run_main({% for item in list_args -%} {{ item[0] }} = {{ item[1] }} {%- if loop.index == list_args|length -%} {%- else %} , {% endif %} {%- endfor %} ):
    print("hello")
    pass

if __name__ == "__main__":
    run_main()
    time.sleep(10)
'''

from jinja2 import Template

class TemplatesInterface:
    name = "test_python3"
    metadata = meta_data
    
class TemplateFactory(object):
    def __init__(self,templates):
            if isinstance(templates,TemplatesInterface):
                self._templates = templates.name
                self._meta_data = templates.metadata
            else:
                raise Exception("you will setting template or base TemplateInterface object")
    def render(self,*args , **kwargs):
        tm = Template(meta_data)
        msg = tm.render(import_modules=["sys","os"],list_args={("runargs1",10),("runargs2","'test'")})
        print(msg)
        return msg
