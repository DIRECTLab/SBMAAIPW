
import pika

class pizza_messages:
    
    def __init__(self):
        # TODO: update this to use the K8 cluster connection instead of localhost
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='pizzatemp')


    def push_message(self, temp):
        """
        Push the newest temperature reading onto the k8 message queue
        """
        self.channel.basic_publish(exchange='', routing_key='pizzatemp', body=f'{temp}')
