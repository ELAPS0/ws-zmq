#!env/bin/python

"""ZMQ publisher payload test"""

import sys
sys.path.append('..')
import time

import zmq
from zmq.asyncio import Context, Poller
import asyncio
import aux



async def events_publish(cn, payload):
    '''
    publish a lot of events
    @cn     number of events for publishing
    @paload even size in bytes
    '''

    ctx = Context.instance()
    pub = ctx.socket(zmq.PUB)
    pub.connect(pub_url)
    print(f'publisher url {pub_url}, counter {cn}')
    #mandatory delay
    time.sleep(1)

    print('start perfomance measureing...')
    evnt = [b'perf', b'perf start1']
    await pub.send_multipart(evnt)
    while cn:
        cn = cn - 1
        evnt = [b'perf', payload]
        await pub.send_multipart(evnt)

    evnt = [b'perf', b'perf stop']
    await pub.send_multipart(evnt)
    print('stop perfomance measureing...')

if __name__ == '__main__':

    if len(sys.argv) == 4:
        print ('up and running...')
        aux.import_from_file(sys.argv[1]+'.py',sys.argv[1])
        pub_url    =  sys.modules[sys.argv[1]].pub_url
        module_name    =  sys.modules[sys.argv[1]].module_name

        print (pub_url)

        cn = int(sys.argv[2])
        pl_size = int(sys.argv[3])
        payload = bytes([0xa5] * pl_size)
        asyncio.get_event_loop().run_until_complete(asyncio.wait([
            events_publish(cn, payload)
        ]))
    else:
        print ('zmq publisher test\nusage: pub_test.py config_name events_number even_size')
