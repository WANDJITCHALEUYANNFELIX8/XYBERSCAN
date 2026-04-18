import socket
import time
import threading

print("=== PORT SCANNER MULTITHREAD ===\n")

target = input("Entrez l'adresse IP (ex: 127.0.0.1) : ")

start_time = time.time()

def scan_port(port):
	sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1) #evite le blocage 1 se conde max
	result = sock.connect_ex((target,port))
	
	if result == 0:
		print(f"✅ Port ouvert : {port}")
	else:
		print(f"⛔️ Port fermé : {port}")	
	
	sock.close()	
	
threads=[]

for port in range(1,10001):
	t= threading.Thread(target=scan_port, args=(port,))
	threads.append(t)
	t.start()
	
for t in threads:
	t.join()
			
end_time=time.time()

print("\nScan terminé.")
print("Temps total :", round(end_time - start_time, 2), "secondes")
