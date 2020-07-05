#!/usr/bin/python3

import socket
import sys
import base64

#CONNECTION WILL BE CLOSED TO SERVER IF THERE IS ANY ERROR IN CONNECTION OR THROUGH KEYBOARD INTERRUPT.....
#IF CONECTION IS CLOSED FROM CLIENT SIDE , THEN ALSO SERVER WILL KEEP ON LISTENING THE CONNECTIONS .....




def exit():
	print("[-] Error!! Exiting....")
	sys.exit()
	
def usage():
	print("[-] Invalid number of arguments...")
	print("Usage--  ./server.py [port_number]\n")
	print("Warning!!! Don't use port that is already in use\n"+
	       "Note:- To use port below 1024 you need root privileges but not recommended to use ")
	sys.exit()

# TO CHECK IF ALL PARAMETER ARE SPECIFIED TO CREATE SOCKET
if len(sys.argv)!=2:
	usage()

smessage = ""
cmessage = ""

# RESLOVING HOSTNAME
try:	
	host="127.0.0.1"
except socket.gaierror:
	print("UNABLE TO RESOLVE HOSTNAME")
	exit()
except :
	print("SOMETHING WENT WRONG" )
	exit()
	
# TO CHECK WEATHER THE PORT_NUMBER IS IN NUMERIC OR NOT
try:
	port=int(sys.argv[1])
except ValueError:
	print("[-] ERROR--  PORT_NUMBER SHOULD BE NUMERIC ")
	exit()
except:
	print("Something went wrong")
	exit()


#CREATING SOCKET
try:
	
	serverSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.gaierror:
	print("UNABLE TO RESOLVE HOSTNAME")
	exit()
except :
	print("SOMETHING WENT WRONG" )
	exit()
else:
	print("IPv4 Socket created Successfully")


# TO RESUSE SOCKET... IT IS DONE BECAUSE IF CONNECTION IS CLOSED DUE TO ANY ERROR THEN MAYBE THE SERVER BINDED IN SOCKET MAYBE LISTENING , SO TO RESUSE THE SOCKET WE USE setsockopt() METHOD
serverSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)


# BINDING IP AND PORT_NUMBER TO SOCKET
try:
	serverSock.bind((host,port))
except socket.error:
	print("Connection error")
	exit()
except:
	print("Something else went wrong")
	exit()
else:
	print(f"Socket binded to {host} and {port} successfully")


# LISTENING FOR CONNECIONS
serverSock.listen(10)
print(f"Listening on port {port} for connections....")

while True:
	
	#ACCEPTING CONNECTION AND TAKING CLIENT PARAMETERS
	try:
		(clientSock, (addr,cport)) =serverSock.accept()
	except socket.gaierror:
		print("Unable to resolve Connection Parameters")
		exit()
	except socket.error:
		print("Connection problem")
		exit()
	except KeyboardInterrupt:
		print(" CLOSING SOCKET...")
		serverSock.close()
		exit()
	except:
		print("Something else went wrong")
		exit()	
	else:
		print(f"Connection accepted from {addr}\n")
	
	mess="Welcome to the Server"
	message=mess.encode()
	
	
	#SENDING MESSAGE TO CLIENT
	# message must be sent in byte string not in string . So  before sending we are encoding the message which will return message in byte form and then encoding it into base64 beore sending 
	try:
		clientSock.send(base64.b64encode(message))
	except socket.error:
		print("Connection problem")
		exit()
	except KeyboardInterrupt:
		print(" CLOSING SOCKET....")
		serverSock.close()
		exit()
	except:
		print("Something else went wrong")
		exit()
	
	while True:
		
		smessage=""
		#RECEIVING MESSAGE FROM CLIENT
		# SENDER has sent message at base64 format so after receiving we have to decode it into byte form and further decode it make it readable
		try:
			cmess=clientSock.recv(2048)
		except socket.gaierror:
			print("Unable to resolve connection parameters..")
			exit()
		except socket.error:
			print("Connection problem")
			exit()
		except KeyboardInterrupt:
			print(" CLOSING SOCKET....")
			serverSock.close()
			exit()
		except:
			print("Something else went wrong")
			exit()
		
		cmessage=base64.b64decode(cmess)
		#TO CHECK IF CLIENT HAS CLOSED CONNECTION OR NOT
		if len(cmessage)!=0:
			print("Client: " + cmessage.decode())
		else:
			print("Connection Closed by Client")
			clientSock.close()
			break;
			
		smess=input("Server:")
		# TO SEND EMPTY MESSAGE SO THAT CONNECTION CAN BE MAINTAINED
		if len(smess)==0:	
			smess=" "
		smessage=smess.encode()	
		clientSock.send(base64.b64encode(smessage))
			
		
	 
	
	




			
