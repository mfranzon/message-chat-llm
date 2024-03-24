import socket
import threading

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
        except Exception as e:
            print(f"Error receiving message from server: {str(e)}")
            break

def send_messages():
    while True:
        try:
            message = input("")
            if message.strip():
                client_socket.send(message.encode("utf-8"))
        except Exception as e:
            print(f"Error sending message to server: {str(e)}")
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5555))
username = input("Enter your username: ")
client_socket.send(username.encode("utf-8"))
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()
send_thread = threading.Thread(target=send_messages)
send_thread.start()
