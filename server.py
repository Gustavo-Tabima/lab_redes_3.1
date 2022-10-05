import socket
import sys
import hashlib
import datetime
import time
#1. Debe implementar el protocolo de control de transmisión (TCP por sus siglas en inglés) para
#transmitir un archivo hacía un cliente
#2. Debe correr sobre una máquina con sistema operativo UbuntuServer 20.04
#3. La aplicación debe soportar al menos 25 conexiones concurrentes. (check)
#4. Debe tener dos archivos disponibles para su envío a los clientes: un archivo de tamaño 100 MB y
#otro de 250 MB. (check)
#5. La aplicación debe permitir seleccionar qué archivo desea transmitir a los clientes conectados y a
#cuántos clientes en simultáneo; a todos se les envía el mismo archivo durante una transmisión. (check)
#6. Debe enviar a cada cliente un valor hash calculado para el archivo transmitido; este valor será usado
#para validar la integridad del archivo enviado en el aplicativo de cliente.(check)
#7. La transferencia de archivos a los clientes definidos en la prueba debe realizarse solo cuando el
#número de clientes indicados estén conectados y el estado de todos sea listo para recibir. (tengo problemas para hacer esto)


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
inp = input('1 Para la file de 100 MB, 2 para la de 250 MB')

if str(inp) == "1":
    archivo = open("data/100.txt","rb" )
elif str(inp) == "2":
    archivo = open("data/250.txt","rb")
else:
    print("ENTRADA INVÁLIDA WTF")
    sys.exit('\033[93m' + 'Afectas las reglas del lab.')

inp = input('a cuantos les quiere enviar esto?')

if int(inp) > 25:
    print("valor de reenvío inválido wtf")
    sys.exit('\033[93m' + 'Afectas las reglas del lab.')
else:
    valor_de_reenvios = int(inp)


# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(25)
valor_de_conexiones = 0

while valor_de_conexiones <= valor_de_reenvios:
    tiempo_inc = time.time()
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    valor_de_conexiones = valor_de_conexiones+1
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(4096)
            string_data = data
            print('Su mensaje ha sido recibido')
            if string_data.decode('utf8') == "SYN":
                print('sending data back to the client')
                str_respuesta = "SYN ACK"
                str_respuesta = str_respuesta.encode('utf8')
                connection.send(str_respuesta)
            elif string_data.decode("utf-8") == "ACK":
               str_respuesta = "FILE?"
               str_respuesta = str_respuesta.encode('utf8')
               connection.send(str_respuesta)
               
            elif string_data.decode("utf-8") == "FILE":
              line = archivo.read()
             
              connection.send(line)
              
              str_respuesta = "FINAL"
              str_respuesta = str_respuesta.encode('utf8')
              connection.send(str_respuesta)
              text_valor = str(valor_de_conexiones)
              e = datetime.datetime.now()
              f= open("logs/log"+str(e.month)+"-"+str(e.day)+"-"+str(e.hour)+"-"+str(e.minute)+"-"+str(e.second)+ ".txt","w+")
              f.write(str(archivo.__dir__))
              f.write( "\n" +"Este es el cliente de conexión numero: " + text_valor)
              f.write("\n" +"La entrega del archivo fue exitosa")
              tiempo_fin = time.time()
              f.write("\n" +"El tiempo de entrega fue de " + str((tiempo_fin - tiempo_inc)))
            

                
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
