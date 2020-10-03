import json
import os
import time
import sys

from rsmq import RedisSMQ
from rsmq.cmd import NoMessageInQueue


queue = RedisSMQ(host=os.getenv('REDIS'), qname="home-office-lights")


def handle_msg(strip_manager, msg):
    print("Handling {} message".format(msg['type']))
    if msg['type'] == 'solid-colour':
        strip_manager.solid_color(msg['r'], msg['g'], msg['b'])
    if msg['type'] == 'alert':
        strip_manager.alert(msg['r'], msg['g'], msg['b'])
    if msg['type'] == 'off':
        strip_manager.clear()


def server():
    # This import is scoped so that rpi_ws281x does not need to be installed to send messages
    from strip_manager import StripManager
    strip_manager = StripManager.default()

    queue.deleteQueue().exceptions(False).execute()
    queue.createQueue().execute()

    previous_msg = None
    queue_empty = False
    while True:
        try:
            msg_wrapper = queue.receiveMessage().execute()
            msg = json.loads(msg_wrapper['message'])

            # Save this as the previous message provided this is not an alert/off/on event.
            if msg['type'] != 'alert' and msg['type'] != 'off' and msg['type'] != 'on':
                previous_msg = msg

            # Action the message
            if msg['type'] == 'on':
                # Resume previous message
                handle_msg(strip_manager, previous_msg)
            else:
                # Handle message
                handle_msg(strip_manager, msg)
            queue.deleteMessage(id=msg_wrapper['id']).execute()

            # An alert has been actioned, restore the previous state
            if msg['type'] == 'alert' and previous_msg is not None:
                handle_msg(strip_manager, previous_msg)

            queue_empty = False
        except NoMessageInQueue as e:
            if not queue_empty:
                print("Queue empty")
                queue_empty = True
            try:
                time.sleep(1)
            except KeyboardInterrupt as ki:
                break


def send_command(command):
    queue.sendMessage().message(json.loads(command)).execute()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        server()
    else:
        send_command(sys.argv[1])
