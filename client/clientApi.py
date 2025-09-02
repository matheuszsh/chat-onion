import socket
import threading
from sys import exit
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv() # carrega as variaveis de ambiente


class ClientApi():
    def __init__(self, callback=None):
        self.SHARED_KEY = os.getenv("SHARED_KEY")
        self.cipher = Fernet(self.SHARED_KEY.encode())
        self.stop_thread = threading.Event()
        self.start_send_client_msg_event = threading.Event()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.on_message_callback = callback

    def try_connect(self,nick,server):
        try:
            self.client.connect((server, 80))
            encrypted_nick = self.cipher.encrypt(nick.encode())
            self.client.send(encrypted_nick)

        except:
            return False
        
    def start_receiving(self):
        thread = threading.Thread(target=self.recv_server_msg, daemon=True)
        thread.start()
        
    def recv_server_msg(self):
        while not self.stop_thread.is_set():
            try:
                server_msg = self.cipher.decrypt(self.client.recv(1024)).decode("utf-8")
                if self.on_message_callback:
                    self.on_message_callback(server_msg)
            except:
                break

    def send_client_msg(self, text_msg):
            encrypted_msg = self.cipher.encrypt(text_msg.encode())
            self.client.send(encrypted_msg)
