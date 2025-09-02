import customtkinter as ctk
from tkinter import messagebox
from clientApi import ClientApi


class LoginInterface(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração de janela
        self.title("Onion Chat - Login")
        self.geometry("400x250")

        # Grid principal
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Objeto de conexão
        self.clientObj = ClientApi()

        # Frame central
        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)

        frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Título
        label = ctk.CTkLabel(frame, text="Login", font=("Arial", 20, "bold"))
        label.grid(row=0, column=0, pady=10)

        # Entrada de Nick
        self.entry_nick = ctk.CTkEntry(frame, placeholder_text="Digite seu nick")
        self.entry_nick.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Entrada de Endereço
        self.entry_host = ctk.CTkEntry(frame, placeholder_text="Endereço de conexão")
        self.entry_host.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Botão de Login
        btn_login = ctk.CTkButton(frame, text="Entrar", command=self._on_login)
        btn_login.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

    def _on_login(self):
        """Valida os dados e tenta conectar"""
        nick = self.entry_nick.get().strip()
        host = self.entry_host.get().strip()

        if not nick or not host:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos!")
            return

        if self._try_connect(nick, host):
            self.destroy()  # fecha a tela de login
            chat = ChatInterface(nick, host, self.clientObj)
            chat.mainloop()
        else:
            messagebox.showerror("Erro de conexão", "Não foi possível conectar ao servidor!")

    def _try_connect(self,nick, host) -> bool:
        return self.clientObj.try_connect(nick,host) != False



class ChatInterface(ctk.CTk):
    def __init__(self, nick, host, clientObj):
        super().__init__()

        self.nick = nick
        self.host = host
        self.clientObj = clientObj

        self.clientObj.on_message_callback = self._receive_message
        self.clientObj.start_receiving()

        # Configuração de janela
        self.title(f"Chat-Room-Onion ({nick}@{host})")
        self.geometry("600x500")

        # Grid principal
        self.grid_rowconfigure(0, weight=0) # header
        self.grid_rowconfigure(1, weight=1) # mensagens
        self.grid_rowconfigure(2, weight=0) # input
        self.grid_columnconfigure(0, weight=1)

        # Criar componentes
        self._create_header()
        self._create_messages_area()
        self._create_input_bar()

    def _create_header(self):
        header = ctk.CTkFrame(self, height=50, corner_radius=0)
        header.grid(row=0, column=0, sticky="nsew")
        header.grid_propagate(False)

        label = ctk.CTkLabel(
            header,
            text=f"Conectado como {self.nick} em {self.host}",
            font=("Arial", 18)
        )
        label.pack(pady=10)

    def _create_messages_area(self):
        self.messages_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.messages_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self._add_message("Conexão estabelecida com sucesso!", sender="bot")

    def _create_input_bar(self):
        input_frame = ctk.CTkFrame(self, height=60, corner_radius=0)
        input_frame.grid(row=2, column=0, sticky="nsew")
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=0)
        input_frame.grid_propagate(False)

        self.entry = ctk.CTkEntry(input_frame, placeholder_text="Digite sua mensagem...")
        self.entry.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        send_btn = ctk.CTkButton(input_frame, text="Enviar", command=self._send_message)
        send_btn.grid(row=0, column=1, padx=10, pady=10)

    def _add_message(self, text: str, sender: str = "user"):
        if sender == "user":
            msg = ctk.CTkLabel(self.messages_frame, text=f"{self.nick}: {text}", anchor="e", justify="right")
        else:
            msg = ctk.CTkLabel(self.messages_frame, text=f"{text}", anchor="w", justify="left")

        msg.pack(fill="x", pady=5, padx=10, anchor="w" if sender == "bot" else "e")

    def _send_message(self):
        text = self.entry.get().strip()
        self.clientObj.send_client_msg(text)
        if text:
            self._add_message(text, sender="user")
            self.entry.delete(0, "end")

    def _receive_message(self, msg: str):
        """Chamado pelo ChatClient quando chega mensagem"""
        self.after(0, lambda: self._add_message(msg, sender="server"))

if __name__ == "__main__":
    login = LoginInterface()
    login.mainloop()