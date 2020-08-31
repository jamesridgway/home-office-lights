from rsmq.consumer import RedisSMQConsumer

# define Processor
def processor(id, message, rc, ts):
  # Do something
  return True

# create consumer
consumer = RedisSMQConsumer('my-queue', processor, host='127.0.0.1')

# run consumer
consumer.run()