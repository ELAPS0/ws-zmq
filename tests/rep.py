import traceback

import zmq
import asyncio
from zmq.asyncio import Context

rep_url     = 'tcp://127.0.0.1:5555'
rep = Context.instance().socket(zmq.REP)
rep.bind(rep_url)


async def reply(resp):
    await asyncio.sleep(4)
    await rep.send(resp)
    print ('resp {} has been send'.format(resp.decode('utf-8'))) 

async def do_rep(loop):
    try:
        cnt = 0
        while(True):
            msg = await rep.recv()
            print ('got request #{}: {}'.format(cnt, msg.decode('utf-8')))
            asyncio.ensure_future(reply('initialization {}  done '.format(cnt).encode('utf-8')))
            cnt += 1
    except Exception as e:
            print("Error with sub world")
            print(e)
            print (traceback.format_exc())
            print()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_rep(loop))


