#!/usr/bin/python3

import socket
import sys
import base64

# CONNECTION WILL BE CLOSED TO SERVER IF THERE IS ANY ERROR IN CONNECTION OR THROUGH KEYBOARD INTERRUPT.....


def exit():
	print("Connection closed")
	sys.exit()
	
def usage():
	print("[-] Invalid number of argumnets...\n"+
	      "Usage-- ./Client.py [IP_ADDRESS] [PORT_NUMBER]\n" +
	      "Warning Here port number is the port number of server in which server is running\n")
	exit()

# TO CHECK ALL PARAMETER ARE PROVIDED TO CREATE SOCKET
if(len(sys.argv)!=3):
	usage()

smessage = ""
	
# RESOLVING HOST_NAME
try:
		
	host=sys.argv[1]
except socket.gaierror:
	print("[-] UNABLE TO RESOLVE HOSTNAME")
	exit()
except :
	print("[-] SOMETHING WENT WRONG" )
	exit()
else:
	print("[+] HOSTNAME RESOLVED SUCCESSFULLY")


# TO CHECK PORT_NUMBER IS NUMERIC 	
try:
	port=int(sys.argv[2])
except ValueError:
	print("[-] ERROR--  PORT_NUMBER SHOULD BE NUMERIC ")
	exit()
except:
	print("[-] Something went wrong")
	exit()


#CREATING SOCKET
try:
	
	clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print(f"[+] IPv4 TCP socket created successfully")
except socket.error:
	print("[-] ERROR---  UNABLE TO CREATE SOCKET")
	clientSocket.close()
	exit()
except:
	print("[-] SOMETHING WENT WRONG")
	clientSocket.close()
	exit()



while True:
	
	#CONNECTING TO SERVER
	try:
		clientSocket.connect((host,port))
	except ConnectionRefusedError:
		print("[-] ERROR-- CONNECTION REFUSED ")
		clientSocket.close()
		exit()
	except KeyboardInterrupt:
		print(" [+] CLOSING SOCKET....")
		clientSocket.close()
		exit()	
	except:
		print("[-] SOMETHING WENT WRONG")
		clientSocket.close()
		exit()
	else:
			print(f"[+] Connected to {host} successfully")
	
	#RECEVING MESSAGE FROM SERVER
	# SENDER has sent message at base64 format so after receiving we have to decode it into byte form and further decode it make it readable
	while True:
		
		try:
			smess=clientSocket.recv(2048)
		except socket.error:
			print("[-] CONNECTION ERROR")
			clientSocket.close()
			exit()
		except socket.gaierror:
			print("[-] ERROR-- UNABLE TO RESOLVE MESSAGE")
			clientSocket.close()
			exit()
		except KeyboardInterrupt:
			print(" [+] CLOSING SOCKET....")
			clientSocket.close()
			exit()
		except:
			print("[-] SOMETHNG WENT WRONG")
			clientSocket.close()
			exit()
		
		smessage=base64.b64decode(smess)
		# CHECKING CONNECTION IS CLOSED BY SERVER OR NOT
		if len(smessage)!=0:
			print("Client: " + smessage.decode())
		else:
			print("[-] Connection closed")
			clientSocket.close()
			exit()
			
		#SENDING MESSAGE TO SERVER	
		# message must be sent in byte string not in string . So  before sending we are encoding the message which will return message in byte form and then encoding it into base64 beore sending 
		try:	
			cmess=input("")
		except socket.error:
			print("[-] CONNECTION ERROR")
			clientSocket.close()
			exit()
		except KeyboardInterrupt:
			print(" [-] CLOSING SOCKET....")
			clientSocket.close()
			exit()
			
		# TO SEND EMPTY MESSAGE SO THAT CONNECTION CAN BE MAINTAINED.OTHERWISE CONNECTION WILL  BREAK
		if len(cmess)==0:
			cmess=" "
		cmessage=cmess.encode()
		clientSocket.send(base64.b64encode(cmessage))
		



