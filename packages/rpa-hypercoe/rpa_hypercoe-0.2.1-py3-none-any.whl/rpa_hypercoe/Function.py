################ IMPORTS ################
import requests
import os
import json
import base64
import jsonpickle
import inspect
from datetime import datetime
##########################################



def Start_Status(path):
    try:
        # Capturar dados do arquivo de configuração do bot
        Dados_Json = getBotID(path)
        BOT_ID = Dados_Json['BOT_ID']
        ClientToken = Dados_Json['ClientToken']

        # EndPoint API
        UrlAPIStatus = 'https://hypercoe-api-hml.triasoftware.com.br/api/bot/change-status-by-bot'
        #UrlAPIStatus = 'https://api-app.hypercoe.com/api/bot/change-status-by-bot'
        

        # ID - Active=0, Running=1, Paused=2, Error=3
        BOT_Status = 1
        dados = {'id': BOT_ID, 'status': BOT_Status}

        # Headers da requisição (caso necessário)
        headers = {'Content-Type': 'application/json', 'ClientToken': ClientToken}

        # Realize a requisição
        response = requests.post(UrlAPIStatus, json=dados, headers=headers)

        # Verifique o status da resposta
        if response.status_code == 200:  # 200 indica sucesso
            print("Status do Bot Alterado com sucesso")
        else:
            print("Erro na requisição. Status code:", response.status_code)
            
    except Exception as erro:
        print(f"Erro API Status: ", erro)
        return erro

def End_Status(path):
    try:

        # Capturar dados do arquivo de configuração do bot
        Dados_Json = getBotID(path)
        BOT_ID = Dados_Json['BOT_ID']
        ClientToken = Dados_Json['ClientToken']

        # EndPoint API
        UrlAPIStatus = 'https://hypercoe-api-hml.triasoftware.com.br/api/bot/change-status-by-bot'
        #UrlAPIStatus = 'https://api-app.hypercoe.com/api/bot/change-status-by-bot'

        # ID - Active=0, Running=1, Paused=2, Error=3
        BOT_Status = 0
        dados = {'id': BOT_ID, 'status': BOT_Status}

        # Headers da requisição (caso necessário)
        headers = {'Content-Type': 'application/json', 'ClientToken': ClientToken}

        # Realize a requisição
        response = requests.post(UrlAPIStatus, json=dados, headers=headers)

        # Verifique o status da resposta
        if response.status_code == 200:  # 200 indica sucesso
            print("Status do Bot Alterado com sucesso")
        else:
            print("Erro na requisição. Status code:", response.status_code)

    except Exception as erro:
        print(f"Erro API Status: ", erro)
        return erro


def Error_Status(path):
    try:

        # Capturar dados do arquivo de configuração do bot
        Dados_Json = getBotID(path)
        BOT_ID = Dados_Json['BOT_ID']
        ClientToken = Dados_Json['ClientToken']

        # EndPoint API
        UrlAPIStatus = 'https://hypercoe-api-hml.triasoftware.com.br/api/bot/change-status-by-bot'
        #UrlAPIStatus = 'https://api-app.hypercoe.com/api/bot/change-status-by-bot'

        # ID - Active=0, Running=1, Paused=2, Error=3
        BOT_Status = 3
        dados = {'id': BOT_ID, 'status': BOT_Status}

        # Headers da requisição (caso necessário)
        headers = {'Content-Type': 'application/json', 'ClientToken': ClientToken}

        # Realize a requisição
        response = requests.post(UrlAPIStatus, json=dados, headers=headers)

        # Verifique o status da resposta
        if response.status_code == 200:  # 200 indica sucesso
            print("Status do Bot Alterado com sucesso")
        else:
            print("Erro na requisição. Status code:", response.status_code)

    except Exception as erro:
        print(f"Erro API Status: ", erro)
        return erro

def Log (message,path):
    try:

        # Capturar dados do arquivo de configuração do bot
        Dados_Json = getBotID(path)
        ID_Iteration = Dados_Json['ID_Iteration']
        ClientToken = Dados_Json['ClientToken']

        # True / False
        finalLog = False
        # Level - info=0, warn=1, error=2
        level = 0
        typeError = ''
        fileBase64 = ''
        UrlAPILog = 'https://hypercoe-api-hml.triasoftware.com.br/api/execution/add-log-by-bot'
        #UrlAPILog = 'https://api-app.hypercoe.com/api/execution/add-log-by-bot'
        dataatual = datetime.now()
        date = dataatual.strftime("%Y-%m-%dT%H:%M:%S")


        # Setar variaveis
        dados = {'date': date, 'level': level, 'typeError': typeError, 'message': message, 'fileBase64': fileBase64 ,'iterationId': ID_Iteration, 'finalLog':finalLog}

        # Headers da requisição (caso necessário)
        headers = {'Content-Type': 'application/json', 'ClientToken': ClientToken}

        # Realize a requisição
        response = requests.post(UrlAPILog, json=dados, headers=headers)

        # Verifique o status da resposta
        if response.status_code == 200:  # 200 indica sucesso
            print("Log registrado com sucesso:", message)
        else:
            print("Erro na requisição. Status code:", response.status_code)

    except Exception as erro:
        print(f"Erro API Log: ", erro)
        return erro



def Log_Error (message,path):
    try:

        # Capturar dados do arquivo de configuração do bot
        Dados_Json = getBotID(path)
        ID_Iteration = Dados_Json['ID_Iteration']
        ClientToken = Dados_Json['ClientToken']


        finalLog = False
        # Level - info=0, warn=1, error=2
        level = 1
        typeError = ''
        fileBase64 = ''
        UrlAPILog = 'https://hypercoe-api-hml.triasoftware.com.br/api/execution/add-log-by-bot'
        #UrlAPILog = 'https://api-app.hypercoe.com/api/execution/add-log-by-bot'
        dataatual = datetime.now()
        date = dataatual.strftime("%Y-%m-%dT%H:%M:%S")

        
        # Setar variaveis
        dados = {'date': date, 'level': level, 'typeError': typeError, 'message': message, 'fileBase64': fileBase64 ,'iterationId': ID_Iteration, 'finalLog':finalLog}

        # Headers da requisição (caso necessário)
        headers = {'Content-Type': 'application/json', 'ClientToken': ClientToken}

        # Realize a requisição
        response = requests.post(UrlAPILog, json=dados, headers=headers)

        # Verifique o status da resposta
        if response.status_code == 200:  # 200 indica sucesso
            print("Log registrado com sucesso:", message)
        else:
            print("Erro na requisição. Status code:", response.status_code)

    except Exception as erro:
        print(f"Erro API Log: ", erro)
        return erro


def Log_Attaching_File (message,pathfile,path):
    try:

        # Capturar dados do arquivo de configuração do bot
        Dados_Json = getBotID(path)
        ID_Iteration = Dados_Json['ID_Iteration']
        ClientToken = Dados_Json['ClientToken']


        finalLog = False
        # Level - info=0, warn=1, error=2
        level = 0
        typeError = ''
        UrlAPILog = 'https://hypercoe-api-hml.triasoftware.com.br/api/execution/add-log-by-bot'
        #UrlAPILog = 'https://api-app.hypercoe.com/api/execution/add-log-by-bot'
        dataatual = datetime.now()
        date = dataatual.strftime("%Y-%m-%dT%H:%M:%S")

        #Converter arquivo em Base64 caso tenha dados na variavel
        if len(pathfile) > 4:
            try:
                with open(pathfile, 'rb') as file:
                    arquivo_bytes = file.read()
                # Converter o arquivo para base64
                arquivo_base64 = base64.b64encode(arquivo_bytes).decode('utf-8')
                fileBase64 = arquivo_base64
            except Exception as erro:
                print(f"Erro na tentativa de converter o arquivo em Base64: ", erro)
                fileBase64 = ""
        else:
            fileBase64 = ""

        # Setar variaveis
        dados = {'date': date, 'level': level, 'typeError': typeError, 'message': message, 'fileBase64': fileBase64 ,'iterationId': ID_Iteration, 'finalLog':finalLog}

        # Headers da requisição (caso necessário)
        headers = {'Content-Type': 'application/json', 'ClientToken': ClientToken}

        # Realize a requisição
        response = requests.post(UrlAPILog, json=dados, headers=headers)

        # Verifique o status da resposta
        if response.status_code == 200:  # 200 indica sucesso
            print("Log registrado com sucesso:", message)
        else:
            print("Erro na requisição. Status code:", response.status_code)

    except Exception as erro:
        print(f"Erro API Log: ", erro)
        return erro

def End_Log (message,path):
    try:

        # Capturar dados do arquivo de configuração do bot
        Dados_Json = getBotID(path)
        ID_Iteration = Dados_Json['ID_Iteration']
        ClientToken = Dados_Json['ClientToken']


        finalLog = True
        # Level - info=0, warn=1, error=2
        level = 0
        typeError = ''
        fileBase64 = ''
        UrlAPILog = 'https://hypercoe-api-hml.triasoftware.com.br/api/execution/add-log-by-bot'
        #UrlAPILog = 'https://api-app.hypercoe.com/api/execution/add-log-by-bot'
        dataatual = datetime.now()
        date = dataatual.strftime("%Y-%m-%dT%H:%M:%S")

        # Setar variaveis
        dados = {'date': date, 'level': level, 'typeError': typeError, 'message': message, 'fileBase64': fileBase64 ,'iterationId': ID_Iteration, 'finalLog':finalLog}

        # Headers da requisição (caso necessário)
        headers = {'Content-Type': 'application/json', 'ClientToken': ClientToken}

        # Realize a requisição
        response = requests.post(UrlAPILog, json=dados, headers=headers)

        # Verifique o status da resposta
        if response.status_code == 200:  # 200 indica sucesso
            print("Log registrado com sucesso:", message)
        else:
            print("Erro na requisição. Status code:", response.status_code)

    except Exception as erro:
        print(f"Erro API Log: ", erro)
        return erro



def Iteration(path):
    try:

        # Capturar dados do arquivo de configuração do bot
        Dados_Json = getBotID(path)
        BOT_ID = Dados_Json['BOT_ID']
        ClientToken = Dados_Json['ClientToken']

        UrlAPIExecution = 'https://hypercoe-api-hml.triasoftware.com.br/api/execution/add-execution-by-bot'
        #UrlAPIExecution = 'https://api-app.hypercoe.com/api/execution/add-execution-by-bot'
        
        UrlAPIIteracao = 'https://hypercoe-api-hml.triasoftware.com.br/api/execution/add-iteration-by-bot'
        #UrlAPIIteracao = 'https://api-app.hypercoe.com/api/execution/add-iteration-by-bot'
        
        # ID - Active=0, Running=1, Paused=2, Error=3
        dados = {'botId': BOT_ID}

        # Headers da requisição (caso necessário)
        headers = {'Content-Type': 'application/json', 'ClientToken': ClientToken}

        # Realize a requisição
        response = requests.post(UrlAPIExecution, json=dados, headers=headers)

        # Verifique o status da resposta
        if response.status_code == 200:  # 200 indica sucesso
            result = response.json()
            ExecutionID = result['dados']['id']
        else:
            print("Erro na requisição. Execution code:", response.status_code)

        # Dados que você quer enviar no corpo da requisição (em formato JSON, por exemplo)
        dadosIteracao = {'executionId': ExecutionID}
        
        # Headers da requisição (caso necessário)
        headersIteracao = {'Content-Type': 'application/json', 'ClientToken': ClientToken}

        # Realize a requisição
        responseIteracao = requests.post(UrlAPIIteracao, json=dadosIteracao, headers=headersIteracao)

        # Verifique o status da resposta
        if responseIteracao.status_code == 200:  # 200 indica sucesso
            resultIteracao = responseIteracao.json()
            IteracaoID = resultIteracao['dados']['id']
            print("Iteration ID:", IteracaoID)  # Retorna os dados da resposta em formato JSON
            #return IteracaoID

            # Chamar Função para escrever o IteracaoID no arquivo config.txt para serem utilizadas em outros processos
            write_IteracaoID(IteracaoID)
        else:
            print("Erro na requisição. Iteration code:", responseIteracao.status_code)
                
    except Exception as erro:
            print(f"Erro API Execution: ", erro)
            return erro






def Get_Asset(Name_Asset,path):
    try:
        # Capturar dados do arquivo de configuração do bot
        Dados_Json = getBotID(path)
        ClientToken = Dados_Json['ClientToken']

        UrlAPILog = f'https://hypercoe-api-hml.triasoftware.com.br/api/assets/get-by-name/{Name_Asset}'
        #UrlAPILog = f'https://hypercoe-api-hml.triasoftware.com.br/api/assets/get-by-name/{Name_Asset}'
    
        # Headers da requisição (caso necessário)
        headers = {'Content-Type': 'application/json', 'ClientToken': ClientToken}

        # Realize a requisição
        response = requests.get(UrlAPILog, headers=headers)

        # Verifique o status da resposta
        if response.status_code == 200:  # 200 indica sucesso
            data = jsonpickle.decode(response.text)
            documents = data['dados']
            value = documents['value']
            return value
        else:
            return "Erro na requisição. Status code:", response.status_code

    except Exception as erro:
        return "Erro API Log: ", erro






def getBotID(path):
    #Obtenha o diretório do arquivo
    try:
    
        with open(path, 'r') as arquivo:
            Dados = arquivo.read()
            Dados_Json = json.loads(Dados)
            BOT_ID = Dados_Json['BotId']
            ClientToken = Dados_Json['ClientToken']
            Valores = {'BOT_ID': BOT_ID,
                     'ClientToken': ClientToken}
            return Valores
    except Exception as erro:
        print('Erro na etapa de leitura do config.txt')
        raise Exception('Erro na etapa de leitura do config.txt')


def write_IteracaoID(IteracaoID):
    # Caminho para o arquivo config.txt
    caminho_arquivo = 'config.txt'

    # Abre o arquivo e lê o conteúdo
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            conteudo = arquivo.read()
        # Converte o conteúdo em um dicionário Python
        config_dict = json.loads(conteudo)
    except FileNotFoundError:
        # Se o arquivo não existir, cria um dicionário vazio
        config_dict = {}

    # Verifica se a chave "IteracaoID" já existe no dicionário
    if "IteracaoID" in config_dict:
        # Se a chave já existir, atualiza apenas o valor
        config_dict["IteracaoID"] = f"{IteracaoID}"
    else:
        # Se a chave não existir, adiciona a chave e o valor
        config_dict["IteracaoID"] = f"{IteracaoID}"

    # Escreve o dicionário atualizado de volta para o arquivo config.txt
    with open(caminho_arquivo, 'w') as arquivo:
        json.dump(config_dict, arquivo, indent=4)



