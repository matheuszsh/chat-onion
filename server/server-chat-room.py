import socket
import threading
from user_object import User
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import dynamicSendRecv as sr

stop_thread = threading.Event()

load_dotenv()
SHARED_KEY = os.getenv("SHARED_KEY")

cipher = Fernet(SHARED_KEY.encode())

class server():
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 9001
        self.on_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = []
        self.user_lock = threading.Lock()

    def broadcast(self,user_sender:User=None ,text_msg:str=None, nickname=None, flag=True, default=False):
        for user in self.users:
            if default == True:
                encrypted_msg = cipher.encrypt(text_msg.encode())
                sr.send_msg(user.conn, encrypted_msg)
            elif user != user_sender:
                if flag == False:
                    user_msg = f"The {nickname} has {text_msg}"

                if flag == True:
                    user_msg = f"{user_sender.nickname}: {text_msg}"

                encrypted_msg = cipher.encrypt(user_msg.encode())
                sr.send_msg(user.conn, encrypted_msg)

    def controler_msg(self, user):
        while not stop_thread.is_set():
            try:
                encrypted_msg = sr.recv_msg(user.conn)
                decrypted_msg = cipher.decrypt(encrypted_msg).decode("utf-8")
                self.broadcast(user, decrypted_msg)
            except:
                exit_msg = "disconnected."
                print(f"The {user.nickname} has " + exit_msg)
                with self.user_lock:
                    self.broadcast(user_sender=user,flag=False,nickname=user.nickname, text_msg=exit_msg)
                with self.user_lock:
                    self.users.remove(user)
                break

    def listen_connection(self):
        self.on_server.bind((self.host,self.port))
        self.on_server.listen()
        print("---Server on---")
        while not stop_thread.is_set():
            try:
                conn, data_conn = self.on_server.accept()

                nickname = sr.recv_msg(conn)
                decrypted_nickname = cipher.decrypt(nickname).decode("utf-8")
                print(f"CLIENT {decrypted_nickname} CONNECT: {data_conn}")

                user = User(conn, decrypted_nickname)
                with self.user_lock:
                    self.users.append(user)

                default_msg = f"Welcome {decrypted_nickname}"
                self.broadcast(text_msg=default_msg, default=True)

                threadSession = threading.Thread(target=self.controler_msg, args=(user,))
                threadSession.start()
            
            except ConnectionError as e:
                print("Erro: " +  e)


if __name__ == "__main__":
    process_server = server()
    process_server.listen_connection()
