import pika
import subprocess
import socket

def main():

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='gpuPower')

    def callback(ch, method, properties, body):
        # Send power command to gpu
        
        res = body.split(',')
        if res[0] == 'SET':
            hostname = socket.gethostname()
            power_val = 0
            if hostname == 'carla-MS-7C95': # use gpu1 value
                power_val = res[1]
            elif hostname == 'gaston-System-Product-Name': # use gpu2 value
                power_val = res[2]

            


            command = ['nvidia-smi', '-pl', str(power_val)]
            subprocess.run(command, capture_output=True, text=True)
            
        
    channel.basic_consume(queue='gpuPower', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    main()
