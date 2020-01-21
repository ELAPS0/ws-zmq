#!env/bin/python

"""Example using zmq with asyncio coroutines"""
# Copyright (c) PyZMQ Developers.
# This example is in the public domain (CC-0)

import sys
import time

import zmq
from zmq.asyncio import Context, Poller
import asyncio
import aux


ctx = Context.instance()
def msg_proc(msg):
    '''
    message processor 
    @msg    - zmq message (list of binary string (utf-8))
    @return   - list [topic, response_message]
    '''
    if msg[1] == b'init me':
        return [msg[0], msg[1]+b' processed by ' + module_name.encode('utf-8')]
    
    return [b'broadcast', msg[1]+b' processed'+ module_name.encode('utf-8')]

"""
async def request_handler():
    '''
    client single request handler
    '''
    rep = ctx.socket(zmq.REP)
    rep.connect(rep_url)
    msg = await rep.recv()
    print ('got request {}'.format(msg))
    await rep.send('done') 
"""
async def events_handler():
    '''
    client events handler
    receive from web server, icall processor and transmit result  back as event  
    '''

    pull = ctx.socket(zmq.PULL)
    pull.connect(pull_url)
    poller = Poller()
    poller.register(pull, zmq.POLLIN)

    pub = ctx.socket(zmq.PUB)
    pub.connect(pub_url)
    print(f'publisher url {pub_url}')
    while True:
        events = await poller.poll()
        if pull in dict(events):
            msg = await pull.recv_multipart()
            print (msg)
            reply = msg_proc( msg)
            print (reply)
            await pub.send_multipart(reply)
            print('{}, transmetted'.format(reply))

print ('up and running...')

aux.import_from_file(sys.argv[1]+'.py',sys.argv[1])



pull_url    =  sys.modules[sys.argv[1]].pull_url
pub_url    =  sys.modules[sys.argv[1]].pub_url
module_name    =  sys.modules[sys.argv[1]].module_name

print (pull_url, pub_url)

asyncio.get_event_loop().run_until_complete(asyncio.wait([
    events_handler()
    #,request_handler()
]))
