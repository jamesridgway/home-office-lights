import time
from pprint import pprint

from rsmq import RedisSMQ
from rsmq.cmd import NoMessageInQueue

from strip_manager import StripManager

queue = RedisSMQ(host="192.168.75.243", qname="home-office-lights")

queue.deleteQueue().exceptions(False).execute()
queue.createQueue().execute()

strip_manager = StripManager.default()
while True:
    try:
        msg = queue.receiveMessage().execute()

        if msg['type'] == 'solid-colour':
          strip_manager.solid_color(msg['r'], msg['g'], msg['b'])
        else:
          pprint(msg)
    except NoMessageInQueue as e:
        print("Queue empty")
        try:
            time.sleep(1)
        except KeyboardInterrupt as ki:
            break
