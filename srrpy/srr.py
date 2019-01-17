#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
import json
import logging
import random
import string
import sys
import time

from templates import TemplateFactory
__all__ = [
    'Client',
    'Server',
]

class JSONTransport(object):
    """Cross platform transport."""
    _singleton = None
    @classmethod
    def create(cls):
        if cls._singleton is None:
            cls._singleton = JSONTransport()
        return cls._singleton
    def dumps(self, obj):
        return json.dumps(obj)
    def loads(self, obj):
        return json.loads(obj.decode())

class PickleTransport(object):
    """Only works with Python clients and servers."""
    _singleton = None
    @classmethod
    def create(cls):
        if cls._singleton is None:
            cls._singleton = PickleTransport()
        return cls._singleton
    def dumps(self, obj):
        # Version 2 works for Python 2.3 and later
        return pickle.dumps(obj, protocol=2)
    def loads(self, obj):
        return pickle.loads(obj)

class Base(object):
    def __init__(self,redis_server,transport_queue,timeout,codec_type):
        self._db = redis_server
        self._queue = transport_queue
        self._timeout = timeout
        self._codec_type = codec_type
        if self._codec_type == "json":
            self._codec = JSONTransport.create()
        elif self._codec_type == "pickle":
            self._codec = PickleTransport.create()
        else:
            raise Exception("can not support codec type")
        pass

    def run(self):
        pass
    def call(self):
        pass

    @staticmethod
    def random_str(size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    def request(self,msg):
        req_dict =  {"call":self._queue,
                     "callback":self._callback,
                     "body":msg}
        
        rpc_request = self.encode(req_dict)
        logging.debug('Client RPC: %s' % rpc_request)
        self._db.rpush(self._queue, rpc_request)
        pass

    def fetch(self):
        message_queue,message = self._db.blpop(self._queue)
        logging.debug('Server Request: %s' % message)
        request_dict = self.decode(message)
        self._callback = request_dict["callback"]
        self._db.rpush(self._callback,self.encode(
            {"call":self._callback,
             "callback":None,
             "body":"ok"}
        ))
        return request_dict["body"]
        
    def response(self,msg):
        response_dict = self._codec.decode(msg)
        logging.debug('Client Response: %s' % response_dict)
        return response_dict
        pass

    def decode(self, message):
        return self._codec.loads(message)

    def encode(self, message):
        return self._codec.dumps(message)

class Server(Base):
    # def __init__(self,db,queue,timeout,codec):
    #     super().__init__(db,queue,timeout,codec)
    def run(self):
        self._db.delete(self._queue)
        while True:
            #code_body = self.fetch()
            #logging.info('Server  %s' % code_body)
            exec(compile(self.fetch(),'','exec'))
            #print("abc")
            #logging.debug('Server Error: %s' % code_body)
            pass
            
            time.sleep(3)
    pass

class Client(Base):
    def __init__(self,db,queue,timeout,codec,templates):
        super().__init__(db,queue,timeout,codec)
        self._templates = TemplateFactory(templates)
        self._callback = "%s:rpc:%s"%(self._queue,Base.random_str())
        
    def call(self, *args ,**kwargs):
        send_message = self._templates.render()
        logging.debug('Client Request: %s' % send_message)
        request_message = self.request(send_message)
        pass

    def wait_result(self):
        result = self._db.blpop(self._callback, self._timeout)
        if result is None:
            raise Exception("not found result for wait")

        pass
