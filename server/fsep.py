#ToDo: Implementar Exceções para os casos de erro.
#Considerar criar um novo campo: AUTOR.
#ToDo: procurar alternativas para importação de módulos.

import os
import json
from client.client import DOWNLOAD_DIR

DATA_DIR = os.path.join(os.path.dirname(__file__), "data/files")

def processar_mensagem(mensagem, client_socket):
    try:
        dados = json.loads(mensagem)

        if dados["comando"] == "LISTAR":
            arquivos = os.listdir(DATA_DIR)
            resposta = {"status": "ok", "arquivos": arquivos}
        
        elif dados["comando"] == "ENVIAR":
            nome_arquivo = dados["arquivo"]
            caminho_arquivo = os.path.join(DATA_DIR, os.path.basename(nome_arquivo))
            conteudo = dados["conteudo"]
            with open(caminho_arquivo, "w") as f:
                f.write(conteudo)
            resposta = {"status": "ok", "mensagem": f"Arquivo '{nome_arquivo}' salvo no servidor."}
        
        elif dados["comando"] == "BAIXAR":
            nome_arquivo = dados["arquivo"]
            caminho_arquivo = os.path.join(DATA_DIR, os.path.basename(nome_arquivo))
            caminho_cliente = os.path.join(DOWNLOAD_DIR, os.path.basename(nome_arquivo))
            try:
                with open(caminho_arquivo, "r") as f:
                    conteudo = f.read()
                with open(caminho_cliente, "w") as f:
                    f.write(conteudo)
                resposta = {"status": "ok", "mensagem": f"Arquivo '{nome_arquivo}' baixado com sucesso."}
            except FileNotFoundError:
                resposta = {"status": "erro", "mensagem": "Arquivo não encontrado."}

        else:
            resposta = {"status": "erro", "mensagem": "Comando inválido."}

    except json.JSONDecodeError:
        resposta = {"status": "erro", "mensagem": "Formato de mensagem inválido."}

    client_socket.sendall(json.dumps(resposta).encode()) #Comentar em caso de testes rapidos onde o cliente não é necessário.

# Teste
if __name__ == "__main__":
    print(os.listdir(DATA_DIR))
    processar_mensagem('{"comando": "ENVIAR", "arquivo": "baixar_test.txt", "conteudo": "testando o metodo de baixar para o servidor."}', None)

    processar_mensagem('{"comando": "BAIXAR", "arquivo": "baixar_test.txt"}', None)