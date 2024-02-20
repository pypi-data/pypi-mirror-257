from io import StringIO
import os
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import zipfile

class ImportSIGER():
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
        # Coletando inicialização
        self.url = url_siger
        self.user = usuario
        self.password = senha
        # URLS - Equipamentos
        self.url_barra = self.url + 'Barra' + '/GerarRelatorio'
        self.url_cs = self.url + 'CompensadorSerie' + '/GerarRelatorio'
        self.url_cer = self.url + 'CompensadorEstatico' + '/GerarRelatorio'
        self.url_gerador = self.url + 'Gerador' + '/GerarRelatorio'
        self.url_linha = self.url + 'Linha' + '/GerarRelatorio'
        self.url_mutua = self.url + 'Mutua' + '/GerarRelatorio'
        self.url_robras = self.url + 'RelatorioObras' + '/GerarRelatorio'
        self.url_sbarra = self.url + 'ShuntBarra' + '/GerarRelatorio'
        self.url_slinha = self.url + 'ShuntLinha' + '/GerarRelatorio'
        self.url_trafo = self.url + 'Trafo' + '/GerarRelatorio'
        self.url_trafo_aterra = self.url + 'TrafoAterramento' + '/GerarRelatorio'
        self.url_elo_cc = self.url + 'Elo' + '/GerarRelatorio'
        self.url_barra_cc = self.url + 'BarraCc' + '/GerarRelatorio'
        self.url_linha_cc = self.url + 'LinhaCc' + '/GerarRelatorio'
        self.url_conversor_cacc = self.url + 'Conversor' + '/GerarRelatorio'
        self.url_area = self.url + 'Area' + '/GerarRelatorio'
        self.url_limitetensao = self.url + 'LimiteTensao' + '/GerarRelatorio'
        self.url_base_tensao = self.url + 'BaseTensao' + '/GerarRelatorio'
        #
        self.delay_prop = 0

    ###================================================================================================================
    ###
    ### CÓDIGOS PARA COLETAR DATAFRAMES DO SERVIDOR - ESTRUTURA
    ###
    ###================================================================================================================
    def __get_df_from_url(self, url_df):
        """
        Função básica de converter o endereço contendo o csv em dataframe
        """
        # Criando a sessão
        session = requests.Session()

        # Definindo as urls
        login_url  = self.url + 'Login'

        # Passo 1 - Logar no servidor e obter o token
        login_response = session.get(login_url)
        soup = BeautifulSoup(login_response.text, 'html.parser')
        token = soup.find('input', {'name': '__RequestVerificationToken'})['value']

        # Passo 2 - Definir payload
        payload = {
                    'Username': self.user,
                    'Password': self.password,
                    '__RequestVerificationToken': token
                }

        # Passo 3: Realizar o login
        login_response = session.post(login_url, data=payload)

        # Check se o login deu certo
        if login_response.status_code == 200:
            # Passo 4: Access the desired page after successful login
            data_response = session.get(url_df)
            data = data_response.content.decode('utf-8')

            # Passo 5 - Convert the data string to a DataFrame
            df = pd.read_csv(StringIO(data), sep=';', encoding='utf-8')
        else:
            print(f"O login na url: {self.url} falhou!")

        # Clean up the session when done
        session.close()

        return df

    ###================================================================================================================
    ###
    ### CÓDIGOS PARA COLETAR DATAFRAMES DO SERVIDOR - DATAFRAMES PUROS
    ###
    ###================================================================================================================
    def get_barra(self):
        return self.__get_df_from_url(self.url_barra).dropna(axis=1, how='all')

    def get_cs(self):
        return self.__get_df_from_url(self.url_cs).dropna(axis=1, how='all')

    def get_cer(self):
        return self.__get_df_from_url(self.url_cer).dropna(axis=1, how='all')

    def get_gerador(self):
        return self.__get_df_from_url(self.url_gerador).dropna(axis=1, how='all')

    def get_linha(self):
        return self.__get_df_from_url(self.url_linha).dropna(axis=1, how='all')

    def get_mutua(self):
        return self.__get_df_from_url(self.url_mutua).dropna(axis=1, how='all')

    def get_robras(self):
        return self.__get_df_from_url(self.url_robras).dropna(axis=1, how='all')

    def get_sbarra(self):
        return self.__get_df_from_url(self.url_sbarra).dropna(axis=1, how='all')

    def get_slinha(self):
        return self.__get_df_from_url(self.url_slinha).dropna(axis=1, how='all')

    def get_trafo(self):
        return self.__get_df_from_url(self.url_trafo).dropna(axis=1, how='all')

    def get_trafo_aterramento(self):
        return self.__get_df_from_url(self.url_trafo_aterra).dropna(axis=1, how='all')

    def get_elo_cc(self):
        return self.__get_df_from_url(self.url_elo_cc).dropna(axis=1, how='all')

    def get_barra_cc(self):
        return self.__get_df_from_url(self.url_barra_cc).dropna(axis=1, how='all')

    def get_linha_cc(self):
        return self.__get_df_from_url(self.url_linha_cc).dropna(axis=1, how='all')

    def get_conversor_cacc(self):
        return self.__get_df_from_url(self.url_conversor_cacc).dropna(axis=1, how='all')

    def get_area(self):
        return self.__get_df_from_url(self.url_area).dropna(axis=1, how='all')

    def get_limite_tensao(self):
        return self.__get_df_from_url(self.url_limitetensao).dropna(axis=1, how='all')

    def get_base_tensao(self):
        return self.__get_df_from_url(self.url_base_tensao).dropna(axis=1, how='all')

    ###================================================================================================================
    ###
    ### CÓDIGOS PARA COLETAR DATAFRAMES DO SERVIDOR - DATAFRAMES MANIPULADOS
    ###
    ###================================================================================================================
    def get_all_siger_dfs(self):
        """
        Função avançada de converter os dataframes para um único
        """
        # Criando a sessão
        session = requests.Session()

        # Definindo as urls
        login_url  = self.url + 'Login'

        # Passo 1 - Logar no servidor e obter o token
        login_response = session.get(login_url)
        soup = BeautifulSoup(login_response.text, 'html.parser')
        token = soup.find('input', {'name': '__RequestVerificationToken'})['value']

        # Passo 2 - Definir payload
        payload = {
                    'Username': self.user,
                    'Password': self.password,
                    '__RequestVerificationToken': token
                }

        # Passo 3: Realizar o login
        login_response = session.post(login_url, data=payload)

        # Check se o login deu certo
        if login_response.status_code == 200:
            # Definindo urls dos dataframes a serem acessados
            url_df = [self.url_barra,self.url_cs,self.url_cer,self.url_linha,self.url_mutua,
                      self.url_sbarra,self.url_slinha,self.url_trafo,self.url_gerador]
            names_df = ["barra", "cs", "cer", "linha", "mutua", "sbarra", "slinha", "trafo","gerador"]
            dic_dfs = {}

            for index, url_siger in enumerate(url_df):
                # Passo 4: Access the desired page after successful login
                data_response = session.get(url_siger)
                data = data_response.content.decode('utf-8')

                # Passo 5 - Convert the data string to a DataFrame
                dic_dfs[names_df[index]] = pd.read_csv(StringIO(data), sep=';', encoding='utf-8')

            # Coletando Relatório de Obras original
            data_response = session.get(self.url_robras)
            data = data_response.content.decode('utf-8')
            df_robras_orig = (pd.read_csv(StringIO(data), sep=';', encoding='utf-8'))
            df_robras_orig = df_robras_orig.dropna(axis=1, how='all')
            # df_robras_orig = df_robras_orig.rename(columns={"Código de Obra": "Código de Obra de Entrada", "Data": "Data de Entrada"})
            # df_robras_orig = df_robras_orig.drop('Unnamed: 2', axis=1)
        else:
            print(f"O login na url: {self.url} falhou!")

        # Clean up the session when done
        session.close()

        return df_robras_orig, dic_dfs

    def __extract_coment_singleline(self, comentario, start_com):
        if comentario==comentario:
            index_start = comentario.rfind(start_com)
            index_end = comentario.find("\r\n", index_start)

            value = (comentario[index_start+len(start_com):index_end]).replace(":","").replace("=)","").strip()
            return value
        else:
            return None

    def __get_id_barra(self, barra):
        id_var = f"#{str(barra)}#"
        return id_var

    def __get_id_linha(self, barra_de, barra_para, circuito):
        id_var = f"#{str(barra_de)}#-#{str(barra_para)}#-${str(circuito)}$"
        return id_var

    def __get_id_mutua(self, barra_de_1, barra_para_1, circuito_1, inicio_1, final_1, barra_de_2, barra_para_2, circuito_2, inicio_2, final_2):
        id_var = f"#{str(barra_de_1)}#-#{str(barra_para_1)}#-${str(circuito_1)}$-$%{str(inicio_1)}$-$%{str(final_1)}$-#{str(barra_de_2)}#-#{str(barra_para_2)}#-${str(circuito_2)}$-$%{str(inicio_2)}$-$%{str(final_2)}$"
        return id_var

    def __get_id_sbarra(self, barra, grupo):
        id_var = f"#{str(barra)}#-${str(grupo)}$"
        return id_var

    def __get_id_slinha(self, barra_de, barra_para, circuito, grupo, extremidade):
        id_var = f"#{str(barra_de)}#-#{str(barra_para)}#-${str(circuito)}$-${str(grupo)}$-${str(extremidade)}$"
        return id_var

    def _make_siger_base(self, dic_dfs):
        """
        Função avançada de converter os dataframes para um único
        """
        cols_base = ["Código de Obra de Entrada", "Código de Obra de Saída", "Data de Entrada", "Data de Saída", "Estado"]
        cols_siger = ["Tipo", "ID", "Código de Obra de Entrada", "Código de Obra de Saída", "Data de Entrada", "Data de Saída", "Estado"]

        ## 2.1 BUSCANDO RELATÓRIO DE BARRAS
        cols_id = ["Número"]
        list_cols = cols_id + cols_base
        df_siger_temp = dic_dfs["barra"][list_cols]
        df_siger_temp = df_siger_temp.assign(Tipo='BR')
        df_siger_temp["ID"] = np.vectorize(self.__get_id_barra)(df_siger_temp[cols_id])
        df_siger = df_siger_temp[cols_siger]

        ## 2.2 BUSCANDO RELATÓRIO DE LINHAS
        cols_id = ["Barra De", "Barra Para", "Número"]
        list_cols = cols_id + cols_base
        df_siger_temp = dic_dfs["linha"][list_cols]
        df_siger_temp = df_siger_temp.assign(Tipo='LT')
        df_siger_temp["ID"] = np.vectorize(self.__get_id_linha)(df_siger_temp["Barra De"], df_siger_temp["Barra Para"], df_siger_temp["Número"])
        df_siger = pd.concat([df_siger, df_siger_temp[cols_siger]], ignore_index=True)

        ## 2.3 BUSCANDO RELATÓRIO DE MUTUA
        cols_id = ["Barra De 1", "Barra Para 1", "Número de Circuito 1", "Barra De 2", "Barra Para 2", "Número de Circuito 2", "% Inicial 1", "% Final 1", "% Inicial 2", "% Final 2"]
        list_cols = cols_id + cols_base
        df_siger_temp = dic_dfs["mutua"][list_cols]
        df_siger_temp = df_siger_temp.assign(Tipo='MT')
        df_siger_temp["ID"] = np.vectorize(self.__get_id_mutua)(df_siger_temp["Barra De 1"], df_siger_temp["Barra Para 1"], df_siger_temp["Número de Circuito 1"],
                                                        df_siger_temp["% Inicial 1"], df_siger_temp["% Final 1"],
                                                        df_siger_temp["Barra De 2"], df_siger_temp["Barra Para 2"], df_siger_temp["Número de Circuito 2"],
                                                        df_siger_temp["% Inicial 2"], df_siger_temp["% Final 2"],
                                                        )
        df_siger = pd.concat([df_siger, df_siger_temp[cols_siger]], ignore_index=True)

        ## 2.4 BUSCANDO RELATÓRIO DE SHUNTBARRA
        cols_id = ["Número da Barra", "Número"]
        list_cols = cols_id + cols_base
        df_siger_temp = dic_dfs["sbarra"][list_cols]
        df_siger_temp = df_siger_temp.assign(Tipo='SB')
        df_siger_temp["ID"] = np.vectorize(self.__get_id_sbarra)(df_siger_temp["Número da Barra"], df_siger_temp["Número"])
        df_siger = pd.concat([df_siger, df_siger_temp[cols_siger]], ignore_index=True)

        ## 2.5 BUSCANDO RELATÓRIO DE SHUNTLINHA
        cols_id = ["Barra De", "Barra Para", "Número do Circuito", "Número", "Extremidade"]
        list_cols = cols_id + cols_base
        df_siger_temp = dic_dfs["slinha"][list_cols]
        df_siger_temp = df_siger_temp.assign(Tipo='SL')
        df_siger_temp["ID"] = np.vectorize(self.__get_id_slinha)(df_siger_temp["Barra De"], df_siger_temp["Barra Para"], df_siger_temp["Número do Circuito"], df_siger_temp["Número"], df_siger_temp["Extremidade"])
        df_siger = pd.concat([df_siger, df_siger_temp[cols_siger]], ignore_index=True)

        ## 2.6 BUSCANDO RELATÓRIO DE TRAFO
        cols_id = ["Barra De", "Barra Para", "Número"]
        list_cols = cols_id + cols_base
        df_siger_temp = dic_dfs["trafo"][list_cols]
        df_siger_temp = df_siger_temp.assign(Tipo='TR')
        df_siger_temp["ID"] = np.vectorize(self.__get_id_linha)(df_siger_temp["Barra De"], df_siger_temp["Barra Para"], df_siger_temp["Número"])
        df_siger = pd.concat([df_siger, df_siger_temp[cols_siger]], ignore_index=True)

        ## 2.7 BUSCANDO RELATÓRIO DE CS
        cols_id = ["Barra De", "Barra Para", "Número"]
        list_cols = cols_id + cols_base
        df_siger_temp = dic_dfs["cs"][list_cols]
        df_siger_temp = df_siger_temp.assign(Tipo='CS')
        df_siger_temp["ID"] = np.vectorize(self.__get_id_linha)(df_siger_temp["Barra De"], df_siger_temp["Barra Para"], df_siger_temp["Número"])
        df_siger = pd.concat([df_siger, df_siger_temp[cols_siger]], ignore_index=True)

        ## 2.8 BUSCANDO RELATÓRIO DE CER
        cols_id = ["Número da Barra", "Número"]
        list_cols = cols_id + cols_base
        df_siger_temp = dic_dfs["cer"][list_cols]
        df_siger_temp = df_siger_temp.assign(Tipo='CR')
        df_siger_temp["ID"] = np.vectorize(self.__get_id_sbarra)(df_siger_temp["Número da Barra"], df_siger_temp["Número"])
        df_siger = pd.concat([df_siger, df_siger_temp[cols_siger]], ignore_index=True)
        #
        ## 2.8 BUSCANDO RELATÓRIO DE Gerador
        cols_id = ["Número da Barra", "Número"]
        list_cols = cols_id + cols_base
        df_siger_temp = dic_dfs["gerador"][list_cols]
        df_siger_temp = df_siger_temp.assign(Tipo='GR')
        df_siger_temp["ID"] = np.vectorize(self.__get_id_sbarra)(df_siger_temp["Número da Barra"], df_siger_temp["Número"])
        df_siger = pd.concat([df_siger, df_siger_temp[cols_siger]], ignore_index=True)
        df_siger.to_csv("df_siger.csv", index=False, sep=";", encoding="utf-8-sig")

        return df_siger

    def __create_estado_br(self, nome_area):
        if nome_area == nome_area:
            estado_br = nome_area[:2]
        else:
            estado_br = ""
        return estado_br

    def get_robras_expandido(self):
        df_robras = self.__get_df_from_url(self.url_robras)
        df_robras = df_robras.dropna(axis=1, how='all')

        df_robras["Empreendimento"] = np.vectorize(self.__extract_coment_singleline)(df_robras["Comentário sobre a Obra"], "EMPREENDIMENTO")
        df_robras["Empreendedor"] = np.vectorize(self.__extract_coment_singleline)(df_robras["Comentário sobre a Obra"], "EMPREENDEDOR")
        df_robras["Tipo Obra"] = np.vectorize(self.__extract_coment_singleline)(df_robras["Comentário sobre a Obra"], "TIPO OBRA")
        df_robras["Região"] = np.vectorize(self.__extract_coment_singleline)(df_robras["Comentário sobre a Obra"], "REGIÃO")

        return df_robras

    def get_robras_mod(self):
        """
        Função avançada de converter os dataframes para um único
        """
        df_robras_orig, dic_dfs = self.get_all_siger_dfs()

        # Concatenate and drop duplicates in one step
        dfs_concatenated = pd.concat([df.drop_duplicates(subset=['Código de Obra de Entrada'])[['Código de Obra de Entrada', 'Data de Entrada', 'Estado']] for df in dic_dfs.values()])
        df_rob_mod = dfs_concatenated.drop_duplicates(subset=['Código de Obra de Entrada'])
        df_robras_orig = df_robras_orig[['Código de Obra', 'Data']]
        df_robras_orig = df_robras_orig.rename(columns={'Código de Obra': 'Código de Obra de Entrada', 'Data': 'Data de Entrada'})

        # Concatenate the two dataframes vertically
        combined_df = pd.concat([df_rob_mod, df_robras_orig], ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=['Código de Obra de Entrada'])
        # combined_df = combined_df.drop('Unnamed: 2', axis=1)

        return combined_df

    def get_robras_area(self):
        """
        Função avançada de converter os dataframes para um único
        """
        # Dataframes básicos para início do programa
        df_siger = self.get_base_siger()
        df_area = self.get_area()
        df_barra = self.get_barra()

        ###################################################################################
        # Coletando as primeiras ocorrências de cada um dos códigos de obra de entrada
        df_siger_grouped_ce = df_siger.groupby('Código de Obra de Entrada').first()
        df_siger_grouped_ce['barra_primal'] = df_siger_grouped_ce['ID'].str.split('#').str[1]
        df_siger_grouped_ce.reset_index(drop=False, inplace=True)

        # Coletando as primeiras ocorrências de cada um dos códigos de obra de saída
        df_siger_grouped_cs = df_siger.groupby('Código de Obra de Saída').first()
        df_siger_grouped_cs['barra_primal'] = df_siger_grouped_cs['ID'].str.split('#').str[1]
        df_siger_grouped_cs.reset_index(drop=False, inplace=True)

        # Encontrando códigos de obra que só existem na saída!
        df_siger_grouped_cs_0 = df_siger_grouped_cs[~df_siger_grouped_cs['Código de Obra de Saída'].isin(df_siger_grouped_ce['Código de Obra de Entrada'])]

        ###################################################################################
        # Trabalhando nos códigos de obra de entrada
        ## Acrescento informação de número de Área
        df_barra_ce = df_barra[["Número", "Área"]].copy()
        df_barra_ce = df_barra_ce[~df_barra_ce['Número'].duplicated(keep="first")]
        df_siger_grouped_ce['barra_primal'] = df_siger_grouped_ce['barra_primal'].astype(int)
        df_siger_grouped_ce_1 = df_siger_grouped_ce.merge(df_barra_ce, left_on='barra_primal', right_on='Número', how='left')
        df_siger_grouped_ce_1.drop('Número', axis=1, inplace=True)

        ## Acrescento informação da descrição da Área
        df_siger_grouped_ce_2 = df_siger_grouped_ce_1.merge(df_area, left_on='Área', right_on='Número', how='left')
        df_siger_grouped_ce_2.drop('Número', axis=1, inplace=True)
        df_siger_grouped_ce_2.rename(columns={'Nome': 'Nome da Área', 'barra_primal': 'Barra'}, inplace=True)
        df_siger_grouped_ce_2["Código de Obra"] = df_siger_grouped_ce_2["Código de Obra de Entrada"]
        df_siger_grouped_ce_2["Data"] = df_siger_grouped_ce_2["Data de Entrada"]
        df_siger_grouped_ce_2 = df_siger_grouped_ce_2[["Código de Obra", "Data", "Código de Obra de Entrada", "Código de Obra de Saída", "Data de Entrada",
                                                    "Data de Saída", "Estado", "Área", "Nome da Área"]]


        ###################################################################################
        # Trabalhando nos códigos de obra de saída
        ## Acrescento informação de número de Área
        df_siger_grouped_cs_0.loc[:, 'barra_primal'] = df_siger_grouped_cs_0['barra_primal'].astype(int)
        df_siger_grouped_cs_1 = df_siger_grouped_cs_0.merge(df_barra_ce, left_on='barra_primal', right_on='Número', how='left')
        df_siger_grouped_cs_1.drop('Número', axis=1, inplace=True)

        ## Acrescento informação da descrição da Área
        df_siger_grouped_cs_2 = df_siger_grouped_cs_1.merge(df_area, left_on='Área', right_on='Número', how='left')
        df_siger_grouped_cs_2.drop('Número', axis=1, inplace=True)
        df_siger_grouped_cs_2.rename(columns={'Nome': 'Nome da Área', 'barra_primal': 'Barra'}, inplace=True)
        df_siger_grouped_cs_2["Código de Obra"] = df_siger_grouped_cs_2["Código de Obra de Saída"]
        df_siger_grouped_cs_2["Data"] = df_siger_grouped_cs_2["Data de Saída"]
        df_siger_grouped_cs_2 = df_siger_grouped_cs_2[["Código de Obra", "Data", "Código de Obra de Entrada", "Código de Obra de Saída", "Data de Entrada",
                                                    "Data de Saída", "Estado", "Área", "Nome da Área"]]

        # Concatenate the two DataFrames vertically
        df_robras_area = pd.concat([df_siger_grouped_ce_2, df_siger_grouped_cs_2], axis=0)

        # Gerando as regiões e estados
        # df_robras_area.iloc[:]["Estado BR"] = np.vectorize(self.__create_estado_br)(df_robras_area["Nome da Área"])
        df_robras_area["Estado BR"] = np.vectorize(self.__create_estado_br)(df_robras_area["Nome da Área"])

        return df_robras_area

    def get_base_siger(self):
        """
        Função avançada de converter os dataframes para um único
        """
        _, dic_dfs = self.get_all_siger_dfs()

        df_siger = self._make_siger_base(dic_dfs)

        return df_siger
    ###================================================================================================================
    ###
    ### CÓDIGOS PARA BAIXAR DECKS DO SIGER
    ###
    ###================================================================================================================
    def get_decks_from_robras(self, list_robras, progress_bar, workpath, extension=".ALT"):
        """
        Função avançada de converter os dataframes para um único
        """
        path_decks = workpath + "\\TEMP_SIG\\"
        temp_exist = os.path.exists(path_decks)
        if not temp_exist:
            os.makedirs(path_decks)

        # step_pb = (round(100/len(list_robras),0))
        if progress_bar != "":
            progress_bar.setValue(0)
            progress_bar.setRange(0, len(list_robras))

        # Criando a sessão
        session = requests.Session()

        # Definindo as urls
        login_url  = self.url + 'Login'

        # Passo 1 - Logar no servidor e obter o token
        login_response = session.get(login_url)
        soup = BeautifulSoup(login_response.text, 'html.parser')
        token = soup.find('input', {'name': '__RequestVerificationToken'})['value']

        # Passo 2 - Definir payload
        payload = {
                    'Username': self.user,
                    'Password': self.password,
                    '__RequestVerificationToken': token
                }

        # Passo 3: Realizar o login
        login_response = session.post(login_url, data=payload)

        # Check se o login deu certo
        if login_response.status_code == 200:
            dic_decks_pwf = {}
            dic_decks_alt = {}
            counter = 0
            for index, codigo_obra in enumerate(list_robras):
                print(f"Baixando deck {index+1}/{len(list_robras)}")
                if progress_bar != "":
                    progress_bar.setValue(progress_bar.value() + 1)
                # time.sleep(0.05)
                counter += 1
                if counter == 999: counter = 0

                # Definindo urls dos dataframes a serem acessados
                url_zip  = f"{self.url}RelatorioObras/ExportarArquivosEquipamentosObra/{codigo_obra}"

                # Passo 4: Access the desired page after successful login
                data_response = session.get(url_zip)

                if data_response.status_code == 200:
                    # Save the binary data as a zip file
                    try:
                        with open(f"{path_decks}/output_{str(counter)}.zip", "wb") as zip_file:
                            zip_file.write(data_response.content)

                        # Passo 5: Extract the zip file contents
                        with zipfile.ZipFile(f"{path_decks}/output_{str(counter)}.zip", 'r') as zip_file:
                            # Assuming you want to read all CSV files from the zip
                            for file_name in zip_file.namelist():
                                if file_name.upper().endswith("PWF"): #or file_name.endswith(".alt"):
                                    with zip_file.open(file_name) as file:
                                        deck_bin = file.read()
                                        deck_str = deck_bin.decode('cp1252')
                                        dic_decks_pwf[codigo_obra] = deck_str
                                if file_name.upper().endswith("ALT"): #or file_name.endswith(".alt"):
                                    with zip_file.open(file_name) as file:
                                        deck_bin = file.read()
                                        deck_str = deck_bin.decode('cp1252')
                                        dic_decks_alt[codigo_obra] = deck_str
                    except:
                        print(f"Failed to open the zip file from {codigo_obra}! Try again!")
                        pass
                else:
                    print(f"Failed to download the zip file from {url_zip}")
        else:
            print(f"O login na url: {self.url} falhou!")

        # Clean up the session when done
        session.close()

        return dic_decks_pwf, dic_decks_alt
