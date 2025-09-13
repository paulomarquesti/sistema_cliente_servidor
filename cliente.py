import socket
import numpy as np

# Configurações
HOST = '127.0.0.1'
PORTA = 5000
NUM_MAX = 300
TAMANHO_PACOTE = 10
COLUNAS = 500

def contar_ocorrencias(matriz):
    vetor = np.zeros(NUM_MAX, dtype=np.int32)
    for numero in matriz.flatten():
        vetor[numero - 1] += 1
    return vetor

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORTA))
    print("[CLIENTE] Conectado ao servidor")

    while True:
        # Recebe pacote de 10 linhas
        dados = cliente.recv(TAMANHO_PACOTE * COLUNAS * 4)
        if not dados:
            break

        matriz = np.frombuffer(dados, dtype=np.int32).reshape((TAMANHO_PACOTE, COLUNAS))
        vetor_contagem = contar_ocorrencias(matriz)

        # Envia vetor de contagem
        cliente.sendall(vetor_contagem.tobytes())

    cliente.close()
    print("[CLIENTE] Conexão encerrada")

iniciar_cliente()
