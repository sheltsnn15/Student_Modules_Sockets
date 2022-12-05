import os
import sys

import pika


def main():
    # create a connection to local my_rabbitmq message program
    connection_parameters = pika.ConnectionParameters('localhost')
    # connect to my_rabbitmq
    connection = pika.BlockingConnection(connection_parameters)
    # create a channel for message interactions
    channel = connection.channel()

    # send messages to broker using a queue
    channel.queue_declare(queue="letter_box")

    def on_message_received(channel, method, properties, body):
        print(f" [x] Received new message: {body}")

    # consume messages off the queue
    channel.basic_consume(queue="letter_box",  # queue we want to consume off of
                          auto_ack=True,  # auto acknowledge messages received
                          on_message_callback=on_message_received  # something to do when message received
                          )

    print(f" [x] Started consuming")

    channel.start_consuming()  # will call callback when started consuming


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
