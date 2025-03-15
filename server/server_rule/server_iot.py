import socket
import json
import pika
import math
import time
import threading

delitel = 10

# Пул потоков для нашего сервера
class ClientThread(threading.Thread): 
 
    def __init__(self, conn, details): 
        self.conn = conn
        self.details = details
        threading.Thread.__init__ ( self )

        print (f"[+] New server socket thread started for \t{HOST} : \t{PORT}")
        self.conn.sendall("You connected!".encode('utf-8')) 

    def run(self): 
        queue_br  = ""
        #RabbitMQ
        connect_rabbitmq = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq_server'))# Устанавливаем соединение с сервером RabbitMQ
        channel = connect_rabbitmq.channel()
        while True : 
            json_data = self.conn.recv(1024)
            data = json_data.decode('utf-8')
            if data == 'end':
                print('end') # окончание работы соединения
                break
            if data != '':
                if queue_br == "" :
                  js = json.loads(data) 
                  id_device = js['id_device'] 
                  queue_br = 'rule_control_'+str(math.ceil(id_device/delitel))
                  channel.queue_declare(queue = queue_br)
                # js = json.loads(data)
                # if js['status'] == 0 :
                channel.basic_publish(exchange='', routing_key=queue_br, body=data)
                print(data)  # то что отправляем в монгу и брокер  


if __name__ == '__main__':
    time.sleep(40)

    s = socket.socket()
    #HOST = "localhost"
    HOST = ""
    PORT = 8080
    couter = 150 # Кол-во соединений
    s.bind((HOST, PORT))
    s.listen(couter)    
    
    p = True
    while p == True:  
        (conn, details) = s.accept() 
        ClientThread(conn, details).start()  
