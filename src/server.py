import socket
import threading
import ollama

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    username = client_socket.recv(1024).decode("utf-8").strip()
    print(f"{client_address} is now known as {username}")
    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            if data[:2] == "/$":
                response = ollama.chat(model='mistral', messages=[
                    {
                        'role': 'user',
                        'content': data[2:],
                    },
                    ])
                print(f"Received message from {username}: {data}")
            
                broadcast(f"{username}: {response['message']['content']}", client_socket) 
            elif not data:
                print(f"Connection from {client_address} closed.")
                break
            else:
                print(f"Received message from {username}: {data}")
                
                # Broadcast the received message to all clients except the sender
                broadcast(f"{username}: {data}", client_socket)
        except Exception as e:
            print(f"Error handling client {client_address}: {str(e)}")
            break
    client_socket.close()
    
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode("utf-8"))
            except Exception as e:
                print(f"Error broadcasting message to client: {str(e)}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5555))
server_socket.listen(5)

print("Server listening for connections...")

clients = []

while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)    
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
