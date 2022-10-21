import os
import socket
import threading
import logging
import datetime
import time

buff_size = 1024*16


def send_file(address, filename):

    f = open(filename, "rb")
    data = f.read(buff_size)
    
    time_start = time.time()
    while(data):
        #print(address)
        if(udp_socket.sendto(data, address)):
            data = f.read(buff_size)
            #time.sleep(0.02) # Give receiver a bit time to save
    f.close()
    return time.time() - time_start

def on_new_client(addr, num_cliente, filename):
    logger_s.info(f' Server-Cliente #{num_cliente}:' + 
                 f'Inicio del manejador de envío, la dirección y puerto asociados son {addr}.')
    

         
    logger_s.info(f' Server-Cliente #{num_cliente}:' + 
                 'Enviando el nombre del archivo al cliente.')
    #udp_socket.sendto(filename, address)


    logger_s.info(f' Server-Cliente #{num_cliente}: Enviando archivo...') 
    try:
        tiempo_envio = send_file(addr, filename)
        tiempo_envio = round(tiempo_envio, 5) 
        #print("Llegué hasta acá")
        logger_s.info(f' Server-Cliente #{num_cliente}: Envio finalizado con exito. El tiempo de transferencia fue de {tiempo_envio} segundos.') 
        #udp_socket.sendto(filename, address)

    except:
        logger_s.info(f' Server-Cliente #{num_cliente}: Envio finalizado sin exito.') 
     
   # print("Llegué hasta acá")
    barrier.wait()


now = datetime.datetime.now()
## Creación del logger_s
logging.basicConfig(filename=f'{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}-log.txt', 
                             encoding='utf-8',
                             format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
                             level=logging.INFO,
                             datefmt='%Y-%m-%d %H:%M:%S')
logger_s = logging.getLogger("server_logger")

filename_0 = "archivo_100mb.zip"

filename_1 = "archivo_250mb.zip"
filesize = 0
    
udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)         # Create a socket object
host = socket.gethostname() # Get local machine name
#host = "192.168.9.120"
port = 20001                # Reserve a port for your service.
logger_s.info(f' Server: El servidor {host} en el puerto {port} ha sido inicializado.')
logger_s.info(' Server: Esperando por clientes.')


udp_socket.bind((host, port))        # Bind to the port

lista_clientes = []
num_total_clientes = int(input("Digite el número máximo de conexiones: "))
#num_total_clientes = 4

num_cliente_actual = 1
filename = ""
while num_cliente_actual <= num_total_clientes:
    
    bytesAddressPair = udp_socket.recvfrom(buff_size)

    tipo_archivo_msg = bytesAddressPair[0]
    address = bytesAddressPair[1]
    
    filename = filename_0 if str(tipo_archivo_msg ) == '0' else filename_1
    logger_s.info(f' Server-Cliente #{address}: ' 
                     +  f'El tipo de archivo solicitado por el cliente es {filename} ({tipo_archivo_msg}) cuyo tamaño es de {os.path.getsize(filename)}B .')   
    num_cliente_actual+=1
    lista_clientes.append(address)

i=0

barrier = threading.Barrier(num_total_clientes+1 )
while i < num_total_clientes:
    address = lista_clientes[i]
    th = threading.Thread(target=on_new_client, args=(address, i+1, filename))    
    th.start()   
    i+=1

barrier.wait()
udp_socket.close()