## ToDo List

- [X] Criar Cliente

- [X] Implementar o comando de EXLUIR no `fsep.py`

- [X] Melhorar lógica do comando de ENVIAR no `fsep.py`

- [X] Criar pasta de arquivos enviados no cliente e fazer lógica para armazena-los. -> criação d log csv no cliente (criado assim q o codigo for exec) 

- [ ] Considerar usar interface gráfica em caso do usuário quiser criar e enviar o arquivo na hora, e para que ele não tenha que escrever o conteúdo do arquivo no Terminal.

#### Observações

Como agora o protocolo irá lidar tanto com arquivos texto como arquivos binários diversos, o método de enviar no lado do cliente tem que considerar isso e ser ajustado da melhor maneira no servidor, andei pesquisando e uma boa ideia é usar buffer de transferencias para otimizaçao em casos de arquivos grandes, nao sei ate que ponto isso realmente ajuda. 

⚠️ leitura e escrita binária, "rb", "wb". 