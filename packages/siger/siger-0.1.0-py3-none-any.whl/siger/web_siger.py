import pandas as pd
import numpy as np
from io import StringIO
import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import zipfile
import datetime
import time
from win32com.client import DispatchEx
import win32com.client
from .import_siger import ImportSIGER

class WebSIGER(ImportSIGER):
    r"""Classe destinada a automatizar a extração de dados diretamente do SIGER.

    ...

    Parameters
    ----------
    ...

    Examples
    --------
    Para inicializar a classe, basta chamar ela para o objeto de interesse.

    >>> ...
    >>> ...
    >>> ...
    >>> ...
    """
    ###================================================================================================================
    ###
    ### CÓDIGOS DE INICIALIZAÇÃO
    ###
    ###================================================================================================================
    def __init__(self, url_siger, usuario, senha):
        # Pegando todas as funções da Import_SIGER para uso nesse módulo
        super().__init__(url_siger, usuario, senha)

    ###================================================================================================================
    ###
    ### CÓDIGOS PARA CARREGAR OS 7 ARQUIVOS E WEB ACESSO
    ###
    ###================================================================================================================
    def web_login_siger(self, navegador, user, key):
        # LOGIN
        username = navegador.find_element(By.ID, "Username")
        password = navegador.find_element(By.ID,"Password")
        username.send_keys(user)
        password.send_keys(key)
        xpath = '/html/body/div[3]/main/section/div/div/div/div[2]/div/div/section/form/div[4]/button'
        navegador.find_element(By.XPATH,xpath).click()
        #

    def web_carrega_file_escorregamento(self, navegador, file, commentary, delay):
        ## Acessando a Tela de Escorregamento
        ### Escolhe ADMINISTRAÇÃO
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe ESCORREGAMENTO DE OBRAS
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/ul/li[2]/a'
        navegador.find_element(By.XPATH,xpath).click()
        #
        ## Selecionado opções na Tela de Escorregamento
        ### Marca Opção Possui carimbo de data e obra
        xpath = '//*[@id="PossuiCarimboDataEObra"]'
        navegador.find_element(By.XPATH,xpath).click()
        ### Inserindo Comentário
        xpath = '//*[@id="Comentario"]'
        navegador.find_element(By.XPATH,xpath).send_keys(commentary)
        ### Escolhendo Arquivo
        xpath = '//*[@id="Arquivos"]'
        file_choosen = navegador.find_element(By.XPATH,xpath)
        file_choosen.send_keys(file)
        ### Clicando em Submeter
        xpath = '/html/body/div[3]/main/div/div/form/div/div[2]/button'
        navegador.find_element(By.XPATH,xpath).click()
        time.sleep(delay)
        ### Checando se deu erro!
        xpath = '/html/body/div[3]/div'
        err_msg = navegador.find_element(By.XPATH,xpath).is_displayed()
        if err_msg:
            text_msg = navegador.find_element(By.XPATH,xpath).text
            if text_msg == "×\nNão é possível realizar essa operação, verifique os erros abaixo.\nClique para ver mais" or text_msg =='×\nAlgo inesperado aconteceu!':
                # ctypes.windll.user32.MessageBoxW(0,
                #                             "Atenção! Execução do carregameto suspensa por falha no carregamento do seguinte deck: \n\n" + file +
                #                             "\n\n O processo será encerrado!",
                #                             "Resultado", 1)
                flag_error = True
                return flag_error
        ### Checando se deu erro - 2!
        try:
            xpath = "/html/body/div[3]/div[2]"
            err_msg = navegador.find_element(By.XPATH,xpath).is_displayed()
            if err_msg:
                text_msg = navegador.find_element(By.XPATH,xpath).text
                if text_msg == "×\nNão é possível realizar essa operação, verifique os erros abaixo.\nClique para ver mais" or text_msg =='×\nAlgo inesperado aconteceu!':
                    # ctypes.windll.user32.MessageBoxW(0,
                    #                             "Atenção! Execução do carregameto suspensa por falha no carregamento do seguinte deck: \n\n" + file_1 +
                    #                             "\n\n O processo será encerrado!",
                    #                             "Resultado", 1)
                    flag_error = True
                    return flag_error
        except:
            pass

    def web_carrega_file_importacao_entrada(self, navegador, file, commentary, delay):
        ## Acessando a Importação
        ### Escolhe ADMINISTRAÇÃO
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe Importação
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe Carimbos
        xpath = '//*[@id="PossuiCarimboData"]'
        navegador.find_element(By.XPATH,xpath).click()
        xpath = '//*[@id="PossuiCarimboEstado"]'
        navegador.find_element(By.XPATH,xpath).click()
        ### Inserindo Comentário
        xpath = '//*[@id="Comentario"]'
        navegador.find_element(By.XPATH,xpath).send_keys(commentary)
        ### Escolhendo Arquivo
        xpath = '//*[@id="Arquivos"]'
        file_choosen = navegador.find_element(By.XPATH,xpath)
        file_choosen.send_keys(file)
        ### Clicando em Submeter
        xpath = '//*[@id="submeterbtn"]'
        navegador.find_element(By.XPATH,xpath).click()
        time.sleep(delay)
        ### Checando se deu erro!
        xpath = '/html/body/div[3]/div'
        err_msg = navegador.find_element(By.XPATH,xpath).is_displayed()
        if err_msg:
            text_msg = navegador.find_element(By.XPATH,xpath).text
            if text_msg == "×\nNão é possível realizar essa operação, verifique os erros abaixo.\nClique para ver mais" or text_msg =='×\nAlgo inesperado aconteceu!':
                # ctypes.windll.user32.MessageBoxW(0,
                #                             "Atenção! Execução do carregameto suspensa por falha no carregamento do seguinte deck: \n\n" + file +
                #                             "\n\n O processo será encerrado!",
                #                             "Resultado", 1)
                flag_error = True
                return flag_error
                os._exit(0)
        ### Checando se deu erro - 2!
        try:
            xpath = "/html/body/div[3]/div[2]"
            err_msg = navegador.find_element(By.XPATH,xpath).is_displayed()
            if err_msg:
                text_msg = navegador.find_element(By.XPATH,xpath).text
                if text_msg == "×\nNão é possível realizar essa operação, verifique os erros abaixo.\nClique para ver mais" or text_msg =='×\nAlgo inesperado aconteceu!':
                    # ctypes.windll.user32.MessageBoxW(0,
                    #                             "Atenção! Execução do carregameto suspensa por falha no carregamento do seguinte deck: \n\n" + file +
                    #                             "\n\n O processo será encerrado!",
                    #                             "Resultado", 1)
                    flag_error = True
                    return flag_error
        except:
            pass

    def web_carrega_file_importacao_remocao(self, navegador, file, commentary, delay):
        ### Escolhe ADMINISTRAÇÃO
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe Importação
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Inserindo Comentário
        xpath = '//*[@id="Comentario"]'
        navegador.find_element(By.XPATH,xpath).clear()
        navegador.find_element(By.XPATH,xpath).send_keys(commentary)
        ### Escolhendo Arquivo
        xpath = '//*[@id="Arquivos"]'
        file_choosen = navegador.find_element(By.XPATH,xpath)
        file_choosen.send_keys(file)
        ### Marcando carimbo remoção fisica
        time.sleep(1)
        xpath = '//*[@id="Carga"]/div/div[1]/div[3]/div/div/div/div/div/label[2]'
        navegador.find_element(By.XPATH,xpath).click()
        ### Clicando em Submeter
        xpath = '//*[@id="submeterbtn"]'
        navegador.find_element(By.XPATH,xpath).click()
        ### Confirmando
        time.sleep(3)
        xpath = '/html/body/div[3]/main/div[2]/div/form/div/div[2]/input'
        navegador.find_element(By.XPATH,xpath).click()
        time.sleep(2)
        ### Checando se deu erro!
        xpath = '/html/body/div[3]/div'
        err_msg = navegador.find_element(By.XPATH,xpath).is_displayed()
        if err_msg:
            text_msg = navegador.find_element(By.XPATH,xpath).text
            if text_msg == "×\nNão é possível realizar essa operação, verifique os erros abaixo.\nClique para ver mais" or text_msg =='×\nAlgo inesperado aconteceu!':
                # ctypes.windll.user32.MessageBoxW(0,
                #                             "Atenção! Execução do carregameto suspensa por falha no carregamento do seguinte deck: \n\n" + file +
                #                             "\n\n O processo será encerrado!",
                #                             "Resultado", 1)
                flag_error = True
                return flag_error
        ### Checando se deu erro - 2!
        try:
            xpath = "/html/body/div[3]/div[2]"
            err_msg = navegador.find_element(By.XPATH,xpath).is_displayed()
            if err_msg:
                text_msg = navegador.find_element(By.XPATH,xpath).text
                if text_msg == "×\nNão é possível realizar essa operação, verifique os erros abaixo.\nClique para ver mais" or text_msg =='×\nAlgo inesperado aconteceu!':
                    # ctypes.windll.user32.MessageBoxW(0,
                    #                             "Atenção! Execução do carregameto suspensa por falha no carregamento do seguinte deck: \n\n" + file +
                    #                             "\n\n O processo será encerrado!",
                    #                             "Resultado", 1)
                    flag_error = True
                    return flag_error
        except:
            pass

    def check_escorreg_cascata(self, df_robras_antes, df_robras_depois, file_7):
        df_robras_antes = df_robras_antes.rename(columns={"Data": "Data_antes"})
        df_robras_depois = df_robras_depois.rename(columns={"Data": "Data_depois"})
        df_robras_antes['Data_antes'] = pd.to_datetime(df_robras_antes['Data_antes'], format='%d/%m/%Y')
        df_robras_depois['Data_depois'] = pd.to_datetime(df_robras_depois['Data_depois'], format='%Y-%m-%d')
        df_merged = df_robras_antes.merge(df_robras_depois, on=['Código de Obra'], how='inner')
        #
        df_merged["Alterou_Data"] = np.vectorize(self.__check_change_date)(df_merged["Data_antes"], df_merged["Data_depois"])
        df_data_alterada = df_merged[df_merged["Alterou_Data"] == "S"]
        df_data_alterada = df_data_alterada[["Código de Obra", "Data_antes", "Data_depois"]]
        #
        # Levantamento de datas no arquivo 7
        lista_obras_files = []
        lista_datas_files = []
        with open(file_7, 'r') as file:
            str_data = file.read()
            list_data = str_data.splitlines()
        for i in range(len(list_data)):
            if list_data[i][:13] == "(#SIGER_OBRA:":
                siger_obra = list_data[i][13:].replace('"',"")
                lista_obras_files.append(siger_obra)
            if list_data[i][:12] == "(#SIGER_ESC:":
                siger_data = list_data[i][12:].replace('"',"")
                lista_datas_files.append(siger_data)
        list_file_7 = [lista_obras_files, lista_datas_files]
        list_file_7 = list(map(list, zip(*list_file_7)))
        df_file7 = pd.DataFrame(list_file_7, columns=['Código de Obra', 'Data_Arquivo_7'])
        df_file7['Data_Arquivo_7'] = pd.to_datetime(df_file7['Data_Arquivo_7'], format='%d/%m/%Y')
        #
        df_data_alterada_file7 = df_data_alterada.merge(df_file7, on=['Código de Obra'], how='inner')
        if len(df_data_alterada_file7) > 0:
            df_data_alterada_file7["Alterou_Data_Arqv7"] = np.vectorize(self.__check_change_date)(df_data_alterada_file7["Data_depois"], df_data_alterada_file7["Data_Arquivo_7"])
            df_data_alterada_file7_mod = df_data_alterada_file7[df_data_alterada_file7["Alterou_Data_Arqv7"] == "S"]
        else:
            df_data_alterada_file7_mod = df_data_alterada_file7.copy()

        return df_data_alterada_file7_mod

    def check_apagamento_cascata(self, df_robras_antes, df_robras_depois, file_1, file_4):
        lista_obras_antes = list(df_robras_antes["Código de Obra"].values)
        lista_obras_depois = list(df_robras_depois["Código de Obra"].values)
        lista_obras_removidas = list(set(lista_obras_antes) - set(lista_obras_depois))
        #
        # Buscar nos arquivos 1 e 4 as obras removidas
        lista_obras_files = []
        with open(file_1, 'r') as file:
            str_data = file.read()
            list_data = str_data.splitlines()
        for i in range(len(list_data)):
            if list_data[i][:13] == "(#SIGER_OBRA:":
                siger_obra = list_data[i][13:].replace('"',"").strip()
                lista_obras_files.append(siger_obra)
        with open(file_4, 'r') as file:
            str_data = file.read()
            list_data = str_data.splitlines()
        for i in range(len(list_data)):
            if list_data[i][:20] == "(#SIGER_REMOVE_OBRA:":
                siger_obra = list_data[i][20:].replace('"',"").strip()
                if siger_obra != "REMOVE-1":
                    lista_obras_files.append(siger_obra)

        # Compara Arquivos
        lista_obras_removidas_cascata = [x for x in lista_obras_removidas if x not in lista_obras_files]

        return lista_obras_removidas_cascata

    def check_obras_nao_presentes(self, df_robras_depois, file_5, file_6):
        lista_obras_depois = list(df_robras_depois["Código de Obra"].values)
        #
        # Buscar nos arquivos 1 e 4 as obras removidas
        lista_obras_files = []
        with open(file_5, 'r') as file:
            str_data = file.read()
            list_data = str_data.splitlines()
        for i in range(len(list_data)):
            if list_data[i][:13] == "(#SIGER_OBRA:":
                siger_obra = list_data[i][13:].replace('"',"").strip()
                lista_obras_files.append(siger_obra)

        with open(file_6, 'r') as file:
            str_data = file.read()
            list_data = str_data.splitlines()
        for i in range(len(list_data)):
            if list_data[i][:13] == "(#SIGER_OBRA:":
                siger_obra = list_data[i][13:].replace('"',"").strip()
                lista_obras_files.append(siger_obra)

        # Juntar listas
        lista_obras_files = list(set(lista_obras_files))
        list_missing_obras = [element for element in lista_obras_files if element.upper() not in lista_obras_depois]

        return list_missing_obras

    def __check_change_date(self, data_antes, data_depois):
        if data_antes == data_depois:
            id = "N"
        else:
            id = "S"
        return id

    def carrega_7_arquivos(self, path_decks, chromedriver_path, report_path = "relatorio.txt", start_deck=1, final_deck=7):
        """ Realiza o carregamento automático dos 7 arquivos"""
        # Fotografia do estado atual da base
        df_robras_original = self.get_robras()

        # Coleta lista de decks presentes na pasta
        decks_siger = []
        for filename in os.listdir(path_decks):
            if filename.endswith(('.pwf', '.alt')) or filename.startswith(('1_', '2_', '3_', '4_', '5_', '6_', '7_')):
                decks_siger.append(os.path.join(path_decks, filename))

        # Verifica se estamos com os 7 arquivos para conseguir prosseguir:
        if len(decks_siger) == 7:

            # Inicializa variáveis de conferência de dados
            flag_error = False
            details_error = ""

            # Inicializa o navegador
            service = Service(executable_path=chromedriver_path)
            navegador = webdriver.Chrome(service=service)
            navegador.maximize_window()
            navegador.get(self.url)
            delay = 1

            # Login SIGER
            self.web_login_siger(navegador, self.user, self.password)

            # Arquivo 01 - Escorregamento
            flag_error = self.web_carrega_file_escorregamento(navegador, decks_siger[0], "Arquivo 1 - Escorregamento", delay)
            if flag_error:
                details_error = "Houve um erro no carregamento do arquivo 1!"
                return details_error

            # Arquivo 02 - Importação
            flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[1], "Arquivo 2 - Importação PWF", delay)
            if flag_error:
                details_error = "Houve um erro no carregamento do arquivo 2!"
                return details_error

            # Arquivo 03 - Importação
            flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[2], "Arquivo 3 - Importação ALT", delay)
            if flag_error:
                details_error = "Houve um erro no carregamento do arquivo 3!"
                return details_error

            # Arquivo 04 - Importação
            flag_error = self.web_carrega_file_importacao_remocao(navegador, decks_siger[3], "Arquivo 4 - Remoção Base", delay)
            if flag_error:
                details_error = "Houve um erro no carregamento do arquivo 4!"
                return details_error

            # Arquivo 05 - Importação
            flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[4], "Arquivo 5 - Importação PWF", delay)
            if flag_error:
                details_error = "Houve um erro no carregamento do arquivo 5!"
                return details_error

            # Arquivo 06 - Importação
            flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[5], "Arquivo 6 - Importação ALT", delay)
            if flag_error:
                details_error = "Houve um erro no carregamento do arquivo 6!"
                return details_error

            # Arquivo 07 - Escorregamento
            flag_error = self.web_carrega_file_escorregamento(navegador, decks_siger[6], "Arquivo 7 - Escorregamento", delay)
            if flag_error:
                details_error = "Houve um erro no carregamento do arquivo 7!"
                return details_error

            # Voltando ao menu
            xpath = '/html/body/header/nav/div/a/img'
            navegador.find_element(By.XPATH,xpath).click()
        else:
            print("Não foram encontrados os 7 arquivos na pasta informada. Verificar se há arquivos faltantes ou em excesso!")
            details_error = "Não foram encontrados os 7 arquivos na pasta informada. Verificar se há arquivos faltantes ou em excesso!"
            return details_error

        # Finalizada a execução do carregamento, verificar o resultado obtido
        print("Carregamento concluído com sucesso! Gerando relatório de carregamento...")
        df_robras_mod, dic_dfs = self.__get_all_siger_dfs()
        df_siger = self.__make_siger_base(dic_dfs)
        df_agg = df_siger.groupby(['Código de Obra de Entrada', "Data de Entrada"], as_index=False).agg({'Estado': lambda x: ' '.join(set(x))})
        #
        # PARTE 1 - CHECAR CONJUNTO EXCLUSIVO
        str_exclusivo = self.__aux_check_exclusives(dic_dfs)
        #
        # PARTE 2 - CHECAR ESTADOS MÚLTIPLOS
        df_estado_mult = self.__aux_check_estados_multiplos(df_agg, df_siger)
        #
        # PARTE 3 - CHECAR DATAS MÚLTIPLAS
        df_data_mult = self.__aux_check_datas_multiplas(df_agg)
        #
        # PARTE 4 - CHECAR ESTADOS DEFASADOS
        df_estado_def = self.__aux_check_estados_defasados(df_agg)
        #
        # PARTE 5 - VERIFICAR ESCORREGAMENTOS EM CASCATA
        df_obras_escorregadas_cascata = self.check_escorreg_cascata(df_robras_original, df_robras_mod, decks_siger[6])
        #
        # PARTE 6 - VERIFICAR EXCLUSÕES EM CASCATA
        lista_obras_removidas_cascata = self.check_apagamento_cascata(df_robras_original, df_robras_mod, decks_siger[0], decks_siger[3])

        # Crie um arquivo de texto para escrever o relatório
        with open(report_path, 'w') as arquivo:
            data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            arquivo.write(f"# RELATÓRIO DE CARREGAMENTO SIGER - {data_hora}\n\n")

            # Escreva a variável string no arquivo
            arquivo.write("#"*125 + "\n")
            arquivo.write("# CHECAGEM 01 - CONJUNTOS EXCLUSIVOS\n")
            arquivo.write(f"{str_exclusivo}\n\n")

            # Escreva os DataFrames no arquivo
            arquivo.write("#"*125 + "\n")
            arquivo.write("# CHECAGEM 02 - ESTADOS MÚLTIPLOS\n")
            arquivo.write(df_estado_mult.to_string(index=False) + '\n\n')

            arquivo.write("#"*125 + "\n")
            arquivo.write("# CHECAGEM 03 - DATAS MÚLTIPLAS\n")
            arquivo.write(df_data_mult.to_string(index=False) + '\n\n')

            arquivo.write("#"*125 + "\n")
            arquivo.write("# CHECAGEM 04 - ESTADOS DEFASADOS\n")
            arquivo.write(df_estado_def.to_string(index=False) + '\n\n')

            arquivo.write("#"*125 + "\n")
            arquivo.write("# CHECAGEM 05 - OBRAS ESCORREGADAS EM CASCATA\n")
            arquivo.write(df_obras_escorregadas_cascata.to_string(index=False) + '\n\n')

            arquivo.write("#"*125 + "\n")
            arquivo.write("# CHECAGEM 06 - OBRAS APAGADAS EM CASCATA\n")
            arquivo.write("\n".join(lista_obras_removidas_cascata) + '\n\n')

        return

    def carrega_7_arquivos_gui_pt1(self, path_decks, chromedriver_path, carrega_arquivo):
        """ Realiza o carregamento automático dos 7 arquivos"""
        # Fotografia do estado atual da base
        df_robras_original = self.get_robras()

        # Coleta lista de decks presentes na pasta
        decks_siger = []
        for filename in os.listdir(path_decks):
            if filename.endswith(('.pwf', '.alt')) or filename.startswith(('1_', '2_', '3_', '4_', '5_', '6_', '7_')):
                decks_siger.append(os.path.join(path_decks, filename))

        # Verifica se estamos com os 7 arquivos para conseguir prosseguir:
        if len(decks_siger) == 7:

            # Inicializa variáveis de conferência de dados
            flag_error = False
            details_error = ""

            # Inicializa o navegador
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("prefs", {"detach": True})

            # Inicializa o navegador
            service = Service(executable_path=chromedriver_path)
            navegador = webdriver.Chrome(service=service, options=chrome_options)
            # navegador = webdriver.Chrome(service=service)
            navegador.maximize_window()
            navegador.get(self.url)
            delay = 1

            # Login SIGER
            self.web_login_siger(navegador, self.user, self.password)

            # Arquivo 01 - Escorregamento
            if carrega_arquivo[0]:
                flag_error = self.web_carrega_file_escorregamento(navegador, decks_siger[0], "Arquivo 1 - Escorregamento", delay)
                if flag_error:
                    details_error = "Houve um erro no carregamento do arquivo 1!"
                    return details_error, df_robras_original

            # Arquivo 02 - Importação
            if carrega_arquivo[1]:
                flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[1], "Arquivo 2 - Importação PWF", delay)
                if flag_error:
                    details_error = "Houve um erro no carregamento do arquivo 2!"
                    return details_error, df_robras_original

            # Arquivo 03 - Importação
            if carrega_arquivo[2]:
                flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[2], "Arquivo 3 - Importação ALT", delay)
                if flag_error:
                    details_error = "Houve um erro no carregamento do arquivo 3!"
                    return details_error, df_robras_original

            # Arquivo 04 - Importação
            if carrega_arquivo[3]:
                flag_error = self.web_carrega_file_importacao_remocao(navegador, decks_siger[3], "Arquivo 4 - Remoção Base", delay)
                if flag_error:
                    details_error = "Houve um erro no carregamento do arquivo 4!"
                    return details_error, df_robras_original

            # Arquivo 05 - Importação
            if carrega_arquivo[4]:
                flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[4], "Arquivo 5 - Importação PWF", delay)
                if flag_error:
                    details_error = "Houve um erro no carregamento do arquivo 5!"
                    return details_error, df_robras_original

            # Arquivo 06 - Importação
            if carrega_arquivo[5]:
                flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[5], "Arquivo 6 - Importação ALT", delay)
                if flag_error:
                    details_error = "Houve um erro no carregamento do arquivo 6!"
                    return details_error, df_robras_original

            # Arquivo 07 - Escorregamento
            if carrega_arquivo[6]:
                flag_error = self.web_carrega_file_escorregamento(navegador, decks_siger[6], "Arquivo 7 - Escorregamento", delay)
                if flag_error:
                    details_error = "Houve um erro no carregamento do arquivo 7!"
                    return details_error, df_robras_original

            # Voltando ao menu
            xpath = '/html/body/header/nav/div/a/img'
            navegador.find_element(By.XPATH,xpath).click()
        else:
            print("Não foram encontrados os 7 arquivos na pasta informada. Verificar se há arquivos faltantes ou em excesso!")
            details_error = "Não foram encontrados os 7 arquivos na pasta informada. Verificar se há arquivos faltantes ou em excesso!"
            return details_error, df_robras_original

        return details_error, df_robras_original
        # Iniciando as Listas
        list_so_nome_ant = []
        list_so_nome_nov = []

        # Importando deck para variável
        with open(file1, 'r') as file:
            data_list = file.read().splitlines()

        # Tratando deck para dentro dos objetos
        for i in range(len(data_list)):
            # Coleta SIGER OBRA - NOME ANTIGO
            if data_list[i][:13] == "(#SIGER_OBRA:":
                codigo_siger_nome_ant = data_list[i][13:].strip().replace('"',"")
            # Coleta SIGER OBRA - NOME NOVO
            if data_list[i][:23] == "(#SIGER_NOVO_NOME_OBRA:":
                codigo_siger_nome_nov = data_list[i][24:].strip().replace('"',"")
            # Verifica final do escorregamento
            if data_list[i][:5] == "99999":
                # Salvo na lista
                list_so_nome_ant.append(codigo_siger_nome_ant)
                list_so_nome_nov.append(codigo_siger_nome_nov)

                # Limpa variáveis
                codigo_siger_nome_ant = ""
                codigo_siger_nome_nov = ""

        # Aplicando mudança de nomes
        df_siger_renom = df_siger.copy()
        if len(list_so_nome_nov) > 0:
            for i in range(len(list_so_nome_nov)):
                str_ant = list_so_nome_ant[i]
                str_nov = list_so_nome_nov[i]
                #
                df_siger_renom['Código de Obra de Entrada'] = df_siger_renom['Código de Obra de Entrada'].str.replace(str_ant,str_nov)
                df_siger_renom['Código de Obra de Saída'] = df_siger_renom['Código de Obra de Saída'].str.replace(str_ant,str_nov)

        return df_siger_renom
