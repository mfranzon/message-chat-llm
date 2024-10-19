import socket
import sys
import threading
from termcolor import colored

from config import PREFIX, PORT, WELCOME_MSG, ASK_MSG, SUCCESS_MSG


def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if WELCOME_MSG in message:
                print(message)  # If the message is welcome, skip the output >, because the duplicate
            else:
                if ASK_MSG not in message and SUCCESS_MSG not in message:
                    print(f'\n{message}')
                    # print('Type message or just type enter')
        except Exception as e:
            print(colored(f"Error receiving message from server: {str(e)}", 'red'))
            break


def send_messages():
    while True:
        try:
            message = input(">")
            if message.strip():
                if message.startswith(PREFIX):
                    # print asking message for asker
                    print((colored(ASK_MSG, 'yellow')))
                client_socket.send(message.encode("utf-8"))
        except Exception as e:
            print(colored(f"Error sending message to server: {str(e)}", 'red'))
            break


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', PORT))
username = input("Enter your username: ")

client_socket.send(username.encode("utf-8"))

receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)
receive_thread.start()
send_thread.start()
