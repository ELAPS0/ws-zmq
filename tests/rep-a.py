import traceback

import zmq
import asyncio
from zmq.asyncio import Context

rep_url     = 'tcp://127.0.0.1:5555'
rep = Context.instance().socket(zmq.REP)
rep.bind(rep_url)


async def do_rep(loop):
    try:
        cnt = 0
        while(True):
            [magic, service, msg] = await rep.recv_multipart()
            print ('got request #{}: magic {}, service {}, data {}'.format(cnt, magic, service.decode('utf-8'), msg.decode('utf-8')))
            await asyncio.sleep(1)
            await rep.send_multipart( [magic, service, msg+' initialization done '.encode('utf-8')])
            await asyncio.sleep(1)
            cnt += 1
    except Exception as e:
            print("Error with sub world")
            print(e)
            print (traceback.format_exc())
            print()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_rep(loop))


