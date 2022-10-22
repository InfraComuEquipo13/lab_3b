# Echo client program

# importing the hashlib module
import socket
import threading
import time
import logging
import datetime
import os
import select

class ThreadedClient(threading.Thread):
    ### CONSTRUCTOR DE LA CLASE 
    
    def __init__(self,  numcliente, n_conn ,host, port, tipo_archivo, logger):
        threading.Thread.__init__(self)
        
        #declare instance variables       
        self.numcliente= numcliente
        self.host = host
        self.port = port
        self.n_conn = n_conn
        self.tipo_archivo = tipo_archivo
        
        self.serverAddress = (host, port)
        self.buff_size = 1024*16
        
        #Create udp socket
        self.s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        logger.info(f' Cliente #{self.numcliente}: Estableciendo conexión con el servidor.') 
        self.s.connect((self.host, self.port))
        logger.info(f' Cliente #{self.numcliente}: Conexión con el servidor exitosa en el puerto {self.port}.') 


    def run(self):
        #print(str(self.numcliente) + "\n")
        #Codifica el tipo de archivo y se lo envía al servidor.
        bytesToSend  = str.encode(str(self.tipo_archivo))
        self.s.sendto(bytesToSend, self.serverAddress)
        logger.info(f' Cliente #{self.numcliente}: A la espera de que los demás clientes se conecten y envíen el tipo de archivo. Van {barrier.n_waiting}') 
        
        barrier.wait()

        ################################################
    def start_receive_file(self):
        self.filepath = f"ArchivosRecibidos\Cliente{self.numcliente}-Prueba-{self.n_conn}.txt"
        th = threading.Thread(target=self.receive_file, args=(self.s, self.filepath,))
        print(f"Recibiendo archivo en el cliente{self.numcliente}...")
        th.start()
        print(f"Archivo recibido en el cliente{self.numcliente}.")
        #t.join()  


    def receive_file(self, sck: socket.socket, filename):
        file0 = "archivo_100mb.zip"
        file1 = "archivo_250mb.zip"
        file0size= "111085193B"
        file1size= "249224393B"

        if self.tipo_archivo == 0:
            logger.info(f' El nombre del archivo es {file0}. El tamaño real del archivo es de: {file0size}') 
        else: 
            logger.info(f' El nombre del archivo es {file1}. El tamaño real del archivo es de: {file1size}') 

        logger.info(f' Cliente #{self.numcliente}: Inicio de la transferencia del archivo.') 

        
        try:
            #print(filename)
            #data, addr = self.s.recvfrom(self.buff_size)
            #print(filename)
           #if data:
            #    file_name = data.strip()
            time_start = time.time()
            
            
            f = open(filename,'wb')
            
            data,addr = self.s.recvfrom(self.buff_size)
            try:
                while(data):
                    
                    f.write(data)
                    self.s.settimeout(2)
                    data,addr = self.s.recvfrom(self.buff_size)
                    #tamano = self.s.recvfrom(self.buff_size)
                    #print(tamano)
                print(addr)
            except socket.timeout:
                print("Conexión terminada")
                f.close()
            time_end = round(time.time()-time_start, 5)
            logger.info(f' Cliente #{self.numcliente}: El archivo fue recibido con exito. El tiempo de transferencia fue: {time_end} segundos. El tamaño final del archivo recibido es de {os.path.getsize(filename)}') 

        except:
            logger.info(f' Cliente #{self.numcliente}: La transferencia no fue exitosa.') 
       

#SERVER_IP = "192.168.9.103"

barrier = None
n_conn = int(input('Ingrese el número de conexiones: '))
tipo_archivo = int(input('Ingrese "0" si desea recibir un archivo de 100MB y "1" si desea uno de 250MB: '))
#n_conn = 4
#tipo_archivo = "0"

# Creación del logger
## Fecha de la prueba
now = datetime.datetime.now()
#os.mkdir('Logs')

logging.basicConfig(filename=f'Logs\prueba{n_conn}-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}-log.txt', 
                             encoding='utf-8',
                             format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
                             level=logging.INFO,
                             datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("client_logger")

if __name__ == '__main__':

    barrier = threading.Barrier(n_conn+1 )
    
    # Get local machine name
    HOST = socket.gethostname() 
    #HOST = SERVER_IP
    PORT = 20001      
    logger.info(f' AppCliente: Iniciando la aplicación de clientes con el servidor {HOST} en el puerto {PORT}.') 
    
    i=1
    clientes_list = []
    while i <= n_conn:   
        print("Iniciando la conexión del cliente", i)
        logger.info(f' AppCliente: Iniciando la conexión del cliente {i}.') 
        s = ThreadedClient(i, n_conn, HOST, PORT, tipo_archivo, logging)
        s.start()
        clientes_list.append(s)
        i+=1
    print("Todos las conexiones fueron exitosas, listos para iniciar la recepción del archivo.")
    barrier.wait() ## barrier + 1 

    for s in clientes_list:
        s.start_receive_file()