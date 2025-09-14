# Projeto Chat Onion

Uma aplicação de chat que utiliza a rede **Tor** para comunicação anônima entre clientes e servidores.  
O projeto conta com **criptografia simétrica (Fernet)**, **sockets** e uma **interface gráfica simples** feita com `customtkinter`.

---

## 📌 Visão Geral

O **Projeto Chat Onion** permite que múltiplos usuários se comuniquem de forma segura e privada através da rede **Tor**.  
Ele foi desenvolvido com foco em **privacidade, anonimato e simplicidade de uso**.

A arquitetura é dividida em duas partes principais:

- **Client**
- **Server**

---

## 🖥️ Client

O cliente possui três componentes principais:

1. **Interface gráfica**  
   - Implementada com `customtkinter`.
   - Permite ao usuário:
     - Informar seu **nickname**.
     - Inserir o **endereço/chave .onion** do servidor.
     - Enviar e receber mensagens em tempo real.

2. **Módulo de comunicação (API)**  
   - Gerencia a comunicação via **socket** com o servidor Onion.
   - Cuida do envio e recebimento de dados de forma transparente.

3. **Criptografia**  
   - Usa **Fernet** (criptografia simétrica).
   - Garante a **confidencialidade** das mensagens.

4. **DynamicSendRecv**  
   - Módulo customizado para envio e recebimento dinâmico de dados.
   - Diferente da abordagem tradicional (que exige o tamanho fixo de bytes).
   - Facilita a troca de mensagens sem restrições de buffer.

---

## ⚙️ Server

O servidor é composto por uma **classe principal** que gerencia as conexões e a troca de mensagens.  
Seus métodos e responsabilidades são:

- **`listen_connection`**  
  - Escuta novas conexões.  
  - Envia uma mensagem de **boas-vindas** para o cliente.

- **`controler_msg`**  
  - Tenta receber dados de cada host conectado.  
  - Caso falhe:
    - Encerra a conexão.
    - Informa aos demais clientes que o host saiu.

- **`broadcast`**  
  - Responsável por enviar mensagens recebidas a **todos os clientes conectados**.

O servidor utiliza **sockets** e armazena as conexões em atributos internos para controle eficiente.

---

## 🌐 Integração com a Rede Tor

Para que o chat funcione através da rede **Tor**, foram utilizados os seguintes recursos:

- **Tor Expert Bundle**  
  - Disponibilizado no projeto para que os clientes iniciem a conexão com a rede Tor.  

- **Hidden Services (Ubuntu + Tor)**  
  - O servidor foi configurado em um ambiente Ubuntu.
  - Serviços Tor foram ativados para gerar a chave **.onion**.
  - A configuração foi gerenciada com **systemd**.

Dessa forma, o servidor pode aceitar conexões diretas via endereço **.onion**, garantindo anonimato para todos os participantes.

---

## 🚀 Fluxo de Uso

1. **Servidor**  
   - Configura o **hidden service** no Tor.  
   - Inicia o servidor Python.  
   - Obtém o endereço **.onion** gerado.

2. **Cliente**  
   - Inicia o **Tor Expert Bundle**.  
   - Executa a aplicação cliente.  
   - Informa:
     - Seu **nickname**.
     - O **endereço .onion** do servidor.  

3. **Troca de mensagens**  
   - O cliente se conecta ao servidor via rede Tor.  
   - As mensagens são **criptografadas** com Fernet.  
   - O servidor gerencia conexões e repassa mensagens entre os clientes.  

---

## 🔒 Segurança

- Todas as mensagens são **criptografadas** com **Fernet** (chave simétrica).  
- Comunicação via rede **Tor**, garantindo **anonimato** de clientes e servidor.  
- Desconexões são tratadas para evitar falhas ou informações inconsistentes.  

---

## 📜 Conclusão

O **Projeto Chat Onion** demonstra como é possível criar uma aplicação de chat segura e anônima utilizando:
- **Python**  
- **Tor Hidden Services**  
- **Criptografia simétrica**  
- **Sockets**  
- **Interface gráfica leve**  

