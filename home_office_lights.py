import json
import time

from rsmq import RedisSMQ
from rsmq.cmd import NoMessageInQueue

from strip_manager import StripManager

queue = RedisSMQ(host="192.168.75.243", qname="home-office-lights")

queue.deleteQueue().exceptions(False).execute()
queue.createQueue().execute()

strip_manager = StripManager.default()

def handle_msg(msg):
    if msg['type'] == 'solid-colour':
        strip_manager.solid_color(msg['r'], msg['g'], msg['b'])
    if msg['type'] == 'alert':
        strip_manager.solid_color(msg['r'], msg['g'], msg['b'])

previous_msg = None
while True:
    try:
        msg_wrapper = queue.receiveMessage().execute()
        msg = json.loads(msg_wrapper['message'])

        if msg['type'] != 'alert':
            previous_msg = msg

        handle_msg(msg)
        queue.deleteMessage(id=msg_wrapper['id']).execute()

        if msg['type'] == 'alert' and previous_msg is not None:
            handle_msg(previous_msg)

    except NoMessageInQueue as e:
        print("Queue empty")
        try:
            time.sleep(1)
        except KeyboardInterrupt as ki:
            break
