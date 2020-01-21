#!env/bin/python

"""ZMQ publisher payload test"""

import sys
sys.path.append('..')
import time

import zmq
from zmq.asyncio import Context, Poller
import asyncio
import aux


ctx = Context.instance()

async def events_publish():
    '''
    publish a lot of events
    '''

    cn = 100 # number of published events
    pub = ctx.socket(zmq.PUB)
    pub.connect(pub_url)
    print('start perfomance measureing...')
    evnt = [b'perf start', b'1']
    await pub.send_multipart(evnt)
    while cn:
        cn = cn - 1
        evnt = [b'perf', b'1']
        await pub.send_multipart(evnt)
    evnt = [b'perf stop', b'1']
    await pub.send_multipart(evnt)

    print('stop perfomance measureing...')

print ('up and running...')

aux.import_from_file(sys.argv[1]+'.py',sys.argv[1])



pull_url    =  sys.modules[sys.argv[1]].pull_url
pub_url    =  sys.modules[sys.argv[1]].pub_url
module_name    =  sys.modules[sys.argv[1]].module_name

print (pull_url, pub_url)

asyncio.get_event_loop().run_until_complete(asyncio.wait([
    events_publish()
    #,request_handler()
]))
