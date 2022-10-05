import socket
from random import randrange
import datetime
import time
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
tiempo_inc = time.time()
numeroFile = randrange(100)
try:
     
    # Send data
    str_message = "SYN"
    str_message = str_message.encode("utf-8")
    message = str_message
   
    sock.send(message)

    # Look for the response
    amount_received = 0
    amount_expected =2
    while amount_received < amount_expected:

        data = sock.recv(4096)       
        print("Recibido: " + data.decode("utf-8"))
        if(data.decode("utf-8") == "SYN ACK"):
             str_message = "ACK"
             str_message = str_message.encode("utf-8")
             message = str_message
             sock.send(message)
        elif(data.decode("utf-8") == "FINAL"):
                print('closing socket')
                sock.close()
                e = datetime.datetime.now()
                f= open("logs/log"+str(e.month)+"-"+str(e.day)+"-"+str(e.hour)+"-"+str(e.minute)+"-"+str(e.second)+ ".txt","w+")
                
                f.write("\n" +"Este es el cliente de conexión numero: " + str(numeroFile))
                f.write("\n" +"La entrega del archivo fue exitosa")
                tiempo_fin = time.time()
                f.write("\n" +"El tiempo de entrega fue de " + str((tiempo_fin - tiempo_inc)))                
                amount_expected = 100000
        elif(data.decode("utf-8") == "FILE?"):
             str_message = "FILE"
             str_message = str_message.encode("utf-8")
             message = str_message
             sock.send(message)
        else:
          datos = data.decode("utf-8")
          file = open("Rdata/datos_recieved "+str(numeroFile),"w+")
          file.write(datos)
          file.close()
          amount_received += 1  

finally:
    print("FIN DEL LAB PAL CLIENTE")

