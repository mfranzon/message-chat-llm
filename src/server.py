import socket
import threading
import ollama
from termcolor import colored

from config import MODEL_NAME, PORT, WELCOME_MSG, PREFIX, ASK_MSG, SUCCESS_MSG


def handle_client(client_socket, client_address):
	username = client_socket.recv(1024).decode("utf-8").strip()
	print(colored(f"Accepted connection from {client_address} as {username}", 'green'))
	client_socket.send(
		(colored(WELCOME_MSG, 'green')
		 ).encode("utf-8"))
	while True:
		try:
			data = client_socket.recv(1024).decode("utf-8")
			if not data:
				print(colored(f"Connection from {client_address} closed.", 'red'))
				break

			if data.startswith(PREFIX):
				try:
					response = ollama.chat(model=MODEL_NAME, messages=[
						{
							'role': 'user',
							'content': data[2:],
						},
					])
					response_text = response['message']['content']
					broadcast(colored(f"Answer from LLM for {username}: {response_text}", 'blue'), client_socket)
				except Exception as e:
					print(colored(f"Chat model error: {str(e)}", 'red'))
					break
			else:
				broadcast(f"{username}: {data}", client_socket)

		except Exception as e:
			print(colored(f"Error handling client {client_address}: {str(e)}", 'red'))
			break
	clients.remove(client_socket)
	client_socket.close()


def broadcast(message, sender_socket):
	for client in clients:
		if client != sender_socket:
			try:
				client.send(message.encode("utf-8"))
			except Exception as e:
				print(colored(f"Error broadcasting message to client: {str(e)}", 'red'))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', PORT))
server_socket.listen(5)

print(colored("Server listening for connections...", 'blue'))

clients = []
while True:
	client_socket, client_address = server_socket.accept()
	clients.append(client_socket)
	client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
	client_thread.start()
