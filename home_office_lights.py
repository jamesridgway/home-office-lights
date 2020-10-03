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
        strip_manager.alert(msg['r'], msg['g'], msg['b'])
    if msg['type'] == 'off':
        strip_manager.clear()

previous_msg = None
queue_empty = False
while True:
    try:
        msg_wrapper = queue.receiveMessage().execute()
        msg = json.loads(msg_wrapper['message'])

        # Provided this is no an 'alert' or an 'off save this as the previous message
        if msg['type'] != 'alert' and msg['type'] != 'off':
            previous_msg = msg

        # Action the message
        if msg['type'] == 'on':
            handle_msg(previous_msg)
        else:
            handle_msg(msg)
        queue.deleteMessage(id=msg_wrapper['id']).execute()

        # An alert has been actioned, restore the previous state
        if msg['type'] == 'alert' and previous_msg is not None:
            handle_msg(previous_msg)

        queue_empty = False
    except NoMessageInQueue as e:
        if not queue_empty:
            print("Queue empty")
            queue_empty = True
        try:
            time.sleep(1)
        except KeyboardInterrupt as ki:
            break
