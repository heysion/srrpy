#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__meta_data__ = '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

{% for mod in import_modules %}
import {{ mod }}
{% endfor %}

def run_main({% for item in list_args -%} {{ item[0] }} = {{ item[1] }} {%- if loop.index == list_args|length -%} {%- else %} , {% endif %} {%- endfor %} ):
    print("hello")
    pass

run_main()
time.sleep(3)
print("test")
'''
'''
from srrpy import TemplatesInterface

class MyTemplate(TemplatesInterface):
    name = "mytemplate"
    metadata = __meta_data__
'''

from abc import ABCMeta,abstractmethod
from jinja2 import Template

class TemplatesInterface(metaclass=ABCMeta):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def metadata(self):
        pass

class TemplateFactory(object):
    def __init__(self,templates):
        if isinstance(templates,TemplatesInterface):
            if hasattr(templates,"name") and hasattr(templates,"metadata"):
                self._tmpl = templates
            else:
                raise Exception("you will setting name and metadata on your TemplateInterface class")
        else:
            raise Exception("you will setting template or base TemplateInterface object")

    def render(self,**kwargs):
        return Template(self._tmpl.metadata).render(**kwargs)

