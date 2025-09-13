import socket
import threading
import numpy as np
import matplotlib.pyplot as plt
import time

# Configurações
HOST = '127.0.0.1'
PORTA = 5000
TAMANHO_PACOTE = 10
NUM_MAX = 300

# Gerar matriz de 100.000 x 500 com números entre 1 e 300
matriz = np.random.randint(1, NUM_MAX + 1, size=(100000, 500))
indice_atual = 0
lock_indice = threading.Lock()

# Contagem geral
contagem_geral = np.zeros(NUM_MAX, dtype=int)
lock_contagem = threading.Lock()

# Função para enviar pacotes de 10 linhas
def obter_pacote():
    global indice_atual
    with lock_indice:
        if indice_atual + TAMANHO_PACOTE > matriz.shape[0]:
            return None
        pacote = matriz[indice_atual:indice_atual + TAMANHO_PACOTE]
        indice_atual += TAMANHO_PACOTE
        return pacote

# Função para lidar com cada cliente
def lidar_com_cliente(conn, addr):
    global contagem_geral
    print(f"[+] Cliente conectado: {addr}")
    while True:
        pacote = obter_pacote()
        if pacote is None:
            break
        conn.sendall(pacote.tobytes())

        # Espera receber vetor de contagem
        dados = conn.recv(NUM_MAX * 4)
        vetor = np.frombuffer(dados, dtype=np.int32)

        # Atualiza contagem geral com lock
        with lock_contagem:
            contagem_geral += vetor

    conn.close()
    print(f"[-] Cliente desconectado: {addr}")

# Função para atualizar gráfico periodicamente
def atualizar_grafico():
    while True:
        time.sleep(5)
        with lock_contagem:
            plt.clf()
            plt.plot(range(1, NUM_MAX + 1), contagem_geral)
            plt.title("Contagem Geral dos Números")
            plt.xlabel("Número")
            plt.ylabel("Ocorrências")
            plt.pause(0.01)

# Iniciar servidor
def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORTA))
    servidor.listen()
    print(f"[SERVIDOR] Aguardando conexões em {HOST}:{PORTA}")

    # Thread do gráfico
    threading.Thread(target=atualizar_grafico, daemon=True).start()

    while True:
        conn, addr = servidor.accept()
        threading.Thread(target=lidar_com_cliente, args=(conn, addr), daemon=True).start()

# Inicializa o gráfico
plt.ion()
fig, ax = plt.subplots()

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORTA))
    servidor.listen()
    print(f"[SERVIDOR] Aguardando conexões em {HOST}:{PORTA}")

    # Inicia clientes em threads
    threading.Thread(target=aceitar_clientes, args=(servidor,), daemon=True).start()

    # Atualiza gráfico na thread principal
    while True:
        time.sleep(5)
        with lock_contagem:
            ax.clear()
            ax.plot(range(1, NUM_MAX + 1), contagem_geral)
            ax.set_title("Contagem Geral dos Números")
            ax.set_xlabel("Número")
            ax.set_ylabel("Ocorrências")
            plt.pause(0.01)

def aceitar_clientes(servidor):
    while True:
        conn, addr = servidor.accept()
        threading.Thread(target=lidar_com_cliente, args=(conn, addr), daemon=True).start()

iniciar_servidor()

