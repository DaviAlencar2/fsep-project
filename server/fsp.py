import os
import json
import threading
import time
from server.utils import handle_duplicate_files

DATA_FILES_DIR = os.path.join(os.path.dirname(__file__), "data/files")
BUFFER_SIZE = 4096
arquivo_lock = threading.Lock()

def processar_mensagem(mensagem, client_socket):
    try:
        dados = json.loads(mensagem)

        if dados["comando"] == "LISTAR":
            arquivos = os.listdir(DATA_FILES_DIR)
            resposta = {"status": "ok", "arquivos": arquivos}
        
        elif dados["comando"] == "ENVIAR": # usuario enviando arquivo ao servidor
            nome_arquivo = dados["arquivo"]
            data_arquivo = os.path.join(DATA_FILES_DIR, os.path.basename(nome_arquivo))

            try:
                with arquivo_lock:
                    if os.path.exists(data_arquivo):
                        novo_nome = handle_duplicate_files(nome_arquivo,data_arquivo)
                        data_arquivo = os.path.join(DATA_FILES_DIR, os.path.basename(novo_nome))
                    resposta_inicial = {"status":"ok","mensagem":"Iniciando trasferencia para o servidor"}
                    client_socket.sendall(json.dumps(resposta_inicial).encode())

                    with open(data_arquivo,"wb") as arquivo:
                        while True:
                            dados = client_socket.recv(BUFFER_SIZE)
                            if not dados:
                                break
                           
                            if b"<EOF>" in dados:
                                partes = dados.split(b"<EOF>", 1)
                                arquivo.write(partes[0])  
                                break
                            else:
                                arquivo.write(dados)
                    resposta_final = {"status":"ok","mensagem":"Arquivo recebido com sucesso."}
                    client_socket.sendall(json.dumps(resposta_final).encode())
                    return
            except:
                resposta = {"status":"erro"}


        elif dados["comando"] == "DELETAR": # usuario deletando arquivo do servidor
            nome_arquivo = dados["arquivo"]
            data_arquivo = os.path.join(DATA_FILES_DIR, os.path.basename(nome_arquivo))

            try:
                with arquivo_lock:
                    if not os.path.exists(data_arquivo):
                        resposta = {"status":"erro", "mensagem":"Arquivo não encontrado."}
                    else:
                        os.remove(data_arquivo)
                        resposta = {"status":"ok", "mensagem":"Arquivo deletado com sucesso."}
            except:
                resposta = {"status":"erro", "mensagem":"Erro ao deletar arquivo."}


        elif dados["comando"] == "BAIXAR": # usuario baixando arquivo do servidor
            nome_arquivo = dados["arquivo"]
            data_arquivo = os.path.join(DATA_FILES_DIR, os.path.basename(nome_arquivo))
            try:
                with arquivo_lock:
                    if not os.path.exists(data_arquivo):
                        resposta = {"status":"erro", "mensagem":"Arquivo não encontrado."}
                        client_socket.sendall(json.dumps(resposta).encode())
                        return

                    else:
                        resposta_inicial = {"status":"ok", "mensagem":"iniciando download"}
                        client_socket.sendall(json.dumps(resposta_inicial).encode())

                        time.sleep(0.2)

                        with open(data_arquivo,"rb") as file:
                            while True:
                                dados = file.read(4096)
                                if not dados:
                                    break
                                client_socket.sendall(dados)
                        client_socket.sendall(b"<EOF>")
                return
            except:
                resposta = {"status":"erro", "mensagem":"Erro ao enviar arquivo"}

        else:
            resposta = {"status": "erro", "mensagem": "Comando inválido."}

    except json.JSONDecodeError:
        resposta = {"status": "erro", "mensagem": "Formato de mensagem inválido."}

    client_socket.sendall(json.dumps(resposta).encode())