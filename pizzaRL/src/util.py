import pika
import numpy as np


class pizzatemp:
    def __init__(self) -> None:
        self.last_temp = 0

        #TODO: switch out localhost for k8 host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='pizzatemp')
        self.channel.basic_consume(queue='pizzatemp', on_message_callback=self.callback, auto_atk=True)
        self.channel.start_consuming()

    def __del__(self):
        self.connection.close()

    def callback(self, ch, method, properties, body): 
        try:
            self.last_temp = int(body)
        except Exception as e:
            print(e)
            return 0

    def get_pizza_temp(self):
        """
        grab the temperature of the pizza from the message queue
        which is collected by the pi pico
        """
        return self.last_temp


class gpuPowerManager:


    def __init__(self) -> None:
        self.gpu1_power = 0
        self.gpu2_power = 0

        #TODO: switch out localhost for k8 host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='gpuPower')
        self.channel.basic_consume(queue='gpuPower', on_message_callback=self.callback, auto_atk=True)
        self.channel.start_consuming()


    def __del__(self):
        self.connection.close()

    def callback(self, ch, method, properties, body): 
        try:
            # Expect shape (GET,[gpu1_power],[gpu2_power])
            contents = body.split(',')
            if contents[0] == 'GET':
                self.gpu1_power = contents[1]
                self.gpu2_power = contents[2]
        except Exception as e:
            print(e)
            return 0



    def get_gpu_power(self):
        """
        Grab the gpu stats from the k8 message queue for both gpus
    
        @Returns GPU1 temp, GPU2 temp
    
        """
        return self.gpu1_power, self.gpu2_power
    

    def set_gpu_power(self, gpu1, gpu2):
        """
        Send new GPU power to k8 message queue to be set
        in nvidia-smi
            
        puts shape (SET,[gpu1_power],[gpu2_power])

        @Returns - new GPU temp for each GPU
        """
         
        
        new_gpu1_power = np.clip(self.gpu1_power + gpu1, 100, 350)
        new_gpu2_power = np.clip(self.gpu2_power + gpu2, 100, 350)

        body = f"SET,{new_gpu1_power},{new_gpu2_power}"

        #TODO: clip the gpu power between 100 and 350 (limits for both 3090s)
        self.channel.basic_publish(exchange='', routing_key='gpuPower', body=body)


