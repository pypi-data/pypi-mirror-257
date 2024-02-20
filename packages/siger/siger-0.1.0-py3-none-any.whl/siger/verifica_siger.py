import os
import datetime
import pandas as pd
import numpy as np
from win32com.client import DispatchEx
from .import_siger import ImportSIGER

class VerificaSIGER(ImportSIGER):
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
    ### VERIFICAÇÕES PRÉ CARREGAMENTO - DECKS INDIVIDUAIS
    ###
    ###================================================================================================================
    # 01. Verifica erro nas datas
    def __create_dic_erro_data(self, file, df_robras):
        errors_file = []
        #
        with open(file, 'r') as file:
            str_data = file.read()
            list_data = str_data.splitlines()

        # Montando lista com datas no arquivo
        dados_siger_obra = []
        dados_data_siger_obra = []
        dados_estado = ["Pré-Operacional","Carga Inicial","Típico","Como Construído","Acesso","Projeto Básico","Agente Fora da RB"]
        for i in range(len(list_data)):
            if list_data[i][:13] == "(#SIGER_OBRA:":
                dados_siger_obra.append(list_data[i][13:])
            elif list_data[i][:13] == "(#SIGER_DATA:":
                dados_data_siger_obra.append(list_data[i][13:])
                if list_data[i+1][:12] != "(#SIGER_EST:":
                    errors_file.append(f"Atenção! Não foi informado o estado da obra {dados_siger_obra[-1]}!")
            elif list_data[i][:12] == "(#SIGER_EST:":
                siger_estado = list_data[i][13:].strip().replace('"','').replace("'","")
                if siger_estado not in dados_estado:
                    errors_file.append(f"Atenção! O estado da obra {dados_siger_obra[-1]} não está preenchido corretamente ({siger_estado})!")

        # Comparando datas com base siger
        if len(dados_siger_obra) == len(dados_data_siger_obra):
            for i in range(len(dados_siger_obra)):
                codigo_obra_arquiv = dados_siger_obra[i]
                #
                # Verificando data em formato errado
                if dados_data_siger_obra[i][:1] == '"':
                    errors_file.append(f"Atenção! A data da obra {codigo_obra_arquiv} está no formato errado! Favor retirar as aspas em: {dados_data_siger_obra[i]}!")

                # Pegando índice de ocorrência
                index_df = df_robras.index[df_robras['Código de Obra']==codigo_obra_arquiv].tolist()

                if len(index_df) > 0:
                    # Data no servidor:
                    data_servidor = df_robras["Data"].iloc[index_df].iloc[0]
                    # Data no arquivo
                    data_arquivo = dados_data_siger_obra[i]
                    #
                    # Comparando datas
                    if data_servidor != data_arquivo:
                        errors_file.append(f"Atenção! A data da obra {codigo_obra_arquiv} foi alterada nesse arquivo de {data_servidor} para {data_arquivo}! Favor concentrar mudanças de datas apenas no arquivo 7!")

        # Comparando cabeçalhos
        return errors_file

    def analyze_datas_from_folder(self, path_decks):
        # Análise deck a deck
        dic_errors = {}
        df_robras = self.get_robras()
        for index, deck in enumerate(path_decks):
            list_error = self.__create_dic_erro_data(deck, df_robras)
            filename = deck[deck.rfind("/")+1:]

            if len(list_error) > 0:
                dic_errors[filename] = list_error

        return dic_errors

    # 02. Verifica erro nos comentários
    def __create_dic_erro_comment(self, file):
        errors_file = []
        #
        with open(file, 'r') as file:
            str_data = file.read()
            list_data = str_data.splitlines()

        # Montando lista com comentários no arquivo
        dados_com = []
        siger_obra = ""
        for i in range(len(list_data)):
            if list_data[i][:13] == "(#SIGER_OBRA:":
                if siger_obra == "":
                    siger_obra = list_data[i][13:].strip()
                else:
                    # verifica comentário até então
                    if len(dados_com) < 11:
                        # Está faltando coisa nos comentários
                        if not siger_obra.upper().replace('"',"").startswith("BASE_"):
                            errors_file.append(f"Atenção! O comentário da obra {siger_obra} não foi identificado! Favor verificar possível esquecimento!")
                    else:
                        if not any(texto.startswith("(= REGIÃO") for texto in dados_com):
                            errors_file.append(f"Atenção! O comentário da obra {siger_obra} não está preenchido corretamente! Não está preenchida/informada a REGIÃO!")
                        if not any(texto.startswith("(= TIPO OBRA") for texto in dados_com):
                            errors_file.append(f"Atenção! O comentário da obra {siger_obra} não está preenchido corretamente! Não está preenchida/informada o TIPO OBRA!")

                    siger_obra = list_data[i][13:].strip()
                    dados_com = []

            elif list_data[i][:12] == "(#SIGER_COM:":
                dados_com.append(list_data[i][12:])

                if list_data[i].startswith("(#SIGER_COM:(= REGIÃO        :"):
                    regiao_obra = list_data[i].replace("(#SIGER_COM:(= REGIÃO        :","").replace("=)","").strip()
                    if regiao_obra not in ["S+MS", "SECO", "NNE"]:
                        errors_file.append(f"Atenção! A região cadastrada '{regiao_obra}' da obra {siger_obra} é inválida! Favor usar S+MS/SECO/NNE!")

                if ";" in list_data[i]:
                    errors_file.append(f"ERRO! Caracter inválido ';' localizado no campo Comentário da Obra {siger_obra}! Verificar linha:\n {list_data[i]}")

        # Check final do deck
        if len(dados_com) < 11:
            errors_file.append(f"Atenção! O comentário da obra {siger_obra} não está preenchido corretamente!")

        # Comparando cabeçalhos
        return errors_file

    def analyze_comment_from_folder(self, path_decks):
        # Análise deck a deck
        dic_errors = {}
        # df_robras = self.get_robras()
        for index, deck in enumerate(path_decks):
            list_error = []
            filename = deck[deck.rfind("/")+1:]
            if filename.startswith("5_") or filename.startswith("6_"):
                list_error = self.__create_dic_erro_comment(deck)

            if len(list_error) > 0:
                dic_errors[filename] = list_error

        return dic_errors

    ###================================================================================================================
    ###
    ### CÓDIGOS PARA COMPARAÇÃO ENTRE BASES DO ARQUIVO 5 e 6
    ###
    ###================================================================================================================
    def download_base_arquivo5(self, path_siger):
        """
        Função avançada de converter os dataframes para um único
        """
        _, dic_dfs = self.get_all_siger_dfs()

        # Salvando arquivos na pasta
        # encoding = "cp1252"
        encoding = "utf-8-sig"
        dic_dfs["barra"].to_csv(path_siger + "/5_barra.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["cs"].to_csv(path_siger + "/5_cs.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["cer"].to_csv(path_siger + "/5_cer.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["linha"].to_csv(path_siger + "/5_linha.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["sbarra"].to_csv(path_siger + "/5_sbarra.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["slinha"].to_csv(path_siger + "/5_slinha.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["trafo"].to_csv(path_siger + "/5_trafo.csv", index=False, sep=";", encoding=encoding)

        return

    def download_base_arquivo6(self, path_siger):
        """
        Função avançada de converter os dataframes para um único
        """
        _, dic_dfs = self.get_all_siger_dfs()

        # Salvando arquivos na pasta
        # encoding = "cp1252"
        encoding = "utf-8-sig"
        dic_dfs["barra"].to_csv(path_siger + "/6_barra.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["cs"].to_csv(path_siger + "/6_cs.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["cer"].to_csv(path_siger + "/6_cer.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["linha"].to_csv(path_siger + "/6_linha.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["sbarra"].to_csv(path_siger + "/6_sbarra.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["slinha"].to_csv(path_siger + "/6_slinha.csv", index=False, sep=";", encoding=encoding)
        dic_dfs["trafo"].to_csv(path_siger + "/6_trafo.csv", index=False, sep=";", encoding=encoding)

        return

    def get_code_vba(self):
        vba_code = """
        Sub Macro2()
        '
        ' Macro2 Macro
        '
        '
            Dim table As ListObject
            Dim row As Long, col As Long

            Sheets("Comparacao").Select
            On error resume next
            Set table = ActiveSheet.ListObjects("Table1")
            For row = 1 To table.ListRows.Count
                For col = 1 To table.ListColumns.Count
                    If table.DataBodyRange(row, col) <> table.DataBodyRange(row + 1, col) Then
                        If Mid(table.Range(1, col), 1, 6) = "Estado" Then
                            If table.DataBodyRange(row, col - 1) = 0 And table.DataBodyRange(row + 1, col - 1) = 0 Then
                                table.DataBodyRange(row + 1, col).Interior.ColorIndex = 15
                            ElseIf table.DataBodyRange(row, col - 1) = "" And table.DataBodyRange(row + 1, col - 1) = "" Then
                                table.DataBodyRange(row + 1, col).Interior.ColorIndex = 15
                            Else
                                table.DataBodyRange(row + 1, col).Interior.ColorIndex = 6
                            End If
                        Else
                            table.DataBodyRange(row + 1, col).Interior.ColorIndex = 6
                        End If
                    End If
                Next col
                row = row + 1
            Next row
            On error goto 0
        End Sub
        """
        return vba_code

    def plot_table_excel(self, df, title):
        if df.empty:
            title = title[:-5] + "_vazio.xlsx"
        writer = pd.ExcelWriter(title, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Comparacao', startrow=1, header=False, index=False)
        # workbook = writer.book
        worksheet = writer.sheets['Comparacao']
        (max_row, max_col) = df.shape
        # Create a list of column headers, to use in add_table().
        column_settings = [{'header': column} for column in df.columns]
        # Add the Excel table structure. Pandas will add the data.
        worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
        # Make the columns wider for clarity.
        worksheet.set_column(0, max_col - 1, 12)
        # Close the Pandas Excel writer and output the Excel file.
        writer.close()

        # Init Excel and open workbook to insert and run an macro
        if not df.empty:
            xl = DispatchEx("Excel.Application")
            wb = xl.Workbooks.Add(title)

            # Create a new Module and insert the macro code
            vba_code =  self.get_code_vba()
            mod = wb.VBProject.VBComponents.Add(1)
            mod.CodeModule.AddFromString(vba_code)

            # Run the new Macro
            xl.Run("Macro2")

            # Arquivo com macro
            title = title.replace(".xlsx", ".xlsm")
            title = title.replace("/", "\\")
            # Save the workbook and close Excel
            wb.SaveAs(title, FileFormat=52)
            xl.Quit()
            # Save and release handle
            writer.close()
        else:
            xl = DispatchEx("Excel.Application")
            wb = xl.Workbooks.Add(title)

            # Create a new Module and insert the macro code
            # vba_code =  get_code_vba()
            # mod = wb.VBProject.VBComponents.Add(1)
            # mod.CodeModule.AddFromString(vba_code)

            # Run the new Macro
            # xl.Run("Macro2")

            # Arquivo com macro
            title = title.replace(".xlsx", ".xlsm")
            title = title.replace("/", "\\")
            # Save the workbook and close Excel
            wb.SaveAs(title, FileFormat=52)
            xl.Quit()
            # Save and release handle
            writer.close()

    def comp_base_arquivo56(self, path_siger):
        """
        Função avançada de converter os dataframes para um único
        """
        # encoding = "cp1252"
        encoding = "utf-8-sig"
        dic_dfs = {}
        dic_dfs["barra_5"] = pd.read_csv(path_siger + "/5_barra.csv", sep=";", encoding=encoding).drop("Conjunto", axis=1)
        dic_dfs["barra_6"] = pd.read_csv(path_siger + "/6_barra.csv", sep=";", encoding=encoding).drop("Conjunto", axis=1)
        dic_dfs["cs_5"] = pd.read_csv(path_siger + "/5_cs.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Tipo de Disparo","Área"], axis=1)
        dic_dfs["cs_6"] = pd.read_csv(path_siger + "/6_cs.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Tipo de Disparo","Área"], axis=1)
        dic_dfs["cer_5"] = pd.read_csv(path_siger + "/5_cer.csv", sep=";", encoding=encoding).drop("Conjunto", axis=1)
        dic_dfs["cer_6"] = pd.read_csv(path_siger + "/6_cer.csv", sep=";", encoding=encoding).drop("Conjunto", axis=1)
        dic_dfs["linha_5"] = pd.read_csv(path_siger + "/5_linha.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Resistência (R0 %)","Reatância (X0 %)","Comprimento (km)","Área","Suscept. (S0 Mvar)"], axis=1)
        dic_dfs["linha_6"] = pd.read_csv(path_siger + "/6_linha.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Resistência (R0 %)","Reatância (X0 %)","Comprimento (km)","Área","Suscept. (S0 Mvar)"], axis=1)
        dic_dfs["slinha_5"] = pd.read_csv(path_siger + "/5_slinha.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Tipo de Conexão","Resistência Aterramento (%)","Reatância Aterramento (%)","Área"], axis=1)
        dic_dfs["slinha_6"] = pd.read_csv(path_siger + "/6_slinha.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Tipo de Conexão","Resistência Aterramento (%)","Reatância Aterramento (%)","Área"], axis=1)
        dic_dfs["trafo_5"] = pd.read_csv(path_siger + "/5_trafo.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Resistência (R0 %)","Estado Resistência (R0 %)","Reatância (X0 %)","Estado Reatância (X0 %)","Área","Conexao De","Resistência De","Reatância De","Resistência Para","Reatância Para","Defasamento Conexão","Conexao Para"], axis=1)
        dic_dfs["trafo_6"] = pd.read_csv(path_siger + "/6_trafo.csv", sep=";", encoding=encoding).drop(["Conjunto","Nome","Resistência (R0 %)","Estado Resistência (R0 %)","Reatância (X0 %)","Estado Reatância (X0 %)","Área","Conexao De","Resistência De","Reatância De","Resistência Para","Reatância Para","Defasamento Conexão","Conexao Para"], axis=1)
        dic_dfs["sbarra_5"] = pd.read_csv(path_siger + "/5_sbarra.csv", sep=";", encoding=encoding).drop(["Conjunto","Tipo de Conexão","Resistência Seq. Zero (%)","Reatância Aterramento (%)","Área"], axis=1)
        dic_dfs["sbarra_6"] = pd.read_csv(path_siger + "/6_sbarra.csv", sep=";", encoding=encoding).drop(["Conjunto","Tipo de Conexão","Resistência Seq. Zero (%)","Reatância Aterramento (%)","Área"], axis=1)
        #
        # Inicia comparação
        dic_dfs["comp_barra"] = pd.concat([dic_dfs["barra_5"], dic_dfs["barra_6"]]).drop_duplicates(keep=False).sort_values(by=['Número', "Código de Obra de Entrada"])
        dic_dfs["comp_cs"] = pd.concat([dic_dfs["cs_5"], dic_dfs["cs_6"]]).drop_duplicates(keep=False).sort_values(by=['Barra De','Barra Para','Número', "Código de Obra de Entrada"])
        dic_dfs["comp_cer"] = pd.concat([dic_dfs["cer_5"], dic_dfs["cer_6"]]).drop_duplicates(keep=False).sort_values(by=['Número da Barra', "Número", "Código de Obra de Entrada"])
        dic_dfs["comp_linha"] = pd.concat([dic_dfs["linha_5"], dic_dfs["linha_6"]]).drop_duplicates(keep=False).sort_values(by=['Barra De','Barra Para','Número', "Código de Obra de Entrada"])
        dic_dfs["comp_slinha"] = pd.concat([dic_dfs["slinha_5"], dic_dfs["slinha_6"]]).drop_duplicates(keep=False).sort_values(by=['Barra De','Barra Para','Número do Circuito', "Número", "Extremidade",  "Código de Obra de Entrada"])
        dic_dfs["comp_trafo"] = pd.concat([dic_dfs["trafo_5"], dic_dfs["trafo_6"]]).drop_duplicates(keep=False).sort_values(by=['Barra De','Barra Para','Número', "Código de Obra de Entrada"])
        dic_dfs["comp_sbarra"] = pd.concat([dic_dfs["sbarra_5"], dic_dfs["sbarra_6"]]).drop_duplicates(keep=False).sort_values(by=['Número da Barra', "Número", "Código de Obra de Entrada"])
        #
        # Gera arquivo excel comparação na pasta
        files_siger = os.listdir(path_siger)
        try:
            for item in files_siger:
                if item.endswith(".xlsm") or item.endswith(".xlsx"):
                    os.remove( os.path.join(path_siger, item))
        except:
            pass

        if len(dic_dfs["comp_barra"]) > 0: self.plot_table_excel(dic_dfs["comp_barra"], path_siger + "/comp_barra.xlsx")
        if len(dic_dfs["comp_cs"]) > 0: self.plot_table_excel(dic_dfs["comp_cs"], path_siger + "/comp_cs.xlsx")
        if len(dic_dfs["comp_cer"]) > 0: self.plot_table_excel(dic_dfs["comp_cer"], path_siger + "/comp_cer.xlsx")
        if len(dic_dfs["comp_linha"]) > 0: self.plot_table_excel(dic_dfs["comp_linha"], path_siger + "/comp_linha.xlsx")
        if len(dic_dfs["comp_slinha"]) > 0: self.plot_table_excel(dic_dfs["comp_slinha"], path_siger + "/comp_slinha.xlsx")
        if len(dic_dfs["comp_trafo"]) > 0: self.plot_table_excel(dic_dfs["comp_trafo"], path_siger + "/comp_trafo.xlsx")
        if len(dic_dfs["comp_sbarra"]) > 0: self.plot_table_excel(dic_dfs["comp_sbarra"], path_siger + "/comp_sbarra.xlsx")

        files_siger = os.listdir(path_siger)
        for item in files_siger:
            if item.endswith(".xlsx"):
                os.remove( os.path.join(path_siger, item))

        list_report = []
        list_report.append("Relatório de Comparação: \n")
        list_report.append("Comparação BARRA: VERIFICAR!" if len(dic_dfs["comp_barra"]) > 0 else "Comparação BARRA: OK!")
        list_report.append("Comparação CS: VERIFICAR!" if len(dic_dfs["comp_cs"]) > 0 else "Comparação CS: OK!")
        list_report.append("Comparação CER: VERIFICAR!" if len(dic_dfs["comp_cer"]) > 0 else "Comparação CER: OK!")
        list_report.append("Comparação LINHA: VERIFICAR!" if len(dic_dfs["comp_linha"]) > 0 else "Comparação LINHA: OK!")
        list_report.append("Comparação SHUNT_LINHA: VERIFICAR!" if len(dic_dfs["comp_slinha"]) > 0 else "Comparação SHUNT_LINHA: OK!")
        list_report.append("Comparação TRANSFORMADOR: VERIFICAR!" if len(dic_dfs["comp_trafo"]) > 0 else "Comparação TRANSFORMADOR: OK!")
        list_report.append("Comparação SHUNT_BARRA: VERIFICAR!" if len(dic_dfs["comp_sbarra"]) > 0 else "Comparação SHUNT_BARRA: OK!")

        return list_report

    ###================================================================================================================
    ###
    ### VERIFICAÇÕES PÓS CARREGAMENTO - INDIVIDUAIS
    ###
    ###================================================================================================================
    # 01. Conjuntos exclusivos
    def __aux_check_exclusives(self, dic_dfs):
        """
        Função avançada de converter os dataframes para um único
        """
        list_errors = []
        if len(dic_dfs["barra"][dic_dfs["barra"]["Conjunto"] != "Anafas e Anarede"]) > 0:
            list_errors.append("Barra")
        if len(dic_dfs["cs"][dic_dfs["cs"]["Conjunto"] != "Anafas e Anarede"]) > 0:
            list_errors.append("Compensador Série")
        if len(dic_dfs["cer"][dic_dfs["cer"]["Conjunto"] != "Anafas e Anarede"]) > 0:
            list_errors.append("Compensador Estático")
        if len(dic_dfs["linha"][dic_dfs["linha"]["Conjunto"] != "Anafas e Anarede"]) > 0:
            list_errors.append("Linha")
        if len(dic_dfs["slinha"][dic_dfs["slinha"]["Conjunto"] != "Anafas e Anarede"]) > 0:
            list_errors.append("Shunt Linha")
        if len(dic_dfs["trafo"][dic_dfs["trafo"]["Conjunto"] != "Anafas e Anarede"]) > 0:
            list_errors.append("Transformador")
        #
        # SHUNT DE BARRA é um caso a parte
        if len(dic_dfs["sbarra"][dic_dfs["sbarra"]["Conjunto"] != "Anafas e Anarede"]) > 0:
            flag_sb = False
            # Check 1 - Se existir Shunt só no ANAREDE é erro!
            if len(dic_dfs["sbarra"][dic_dfs["sbarra"]["Conjunto"] == "Anarede"]) > 0:
                list_errors.append("Shunt Barra - FP (atenção!)")
            if len(dic_dfs["sbarra"][dic_dfs["sbarra"]["Conjunto"] == "Anafas"]) > 0:
                list_errors.append("Shunt Barra - CC (esperado!)")

        if len(list_errors) > 0:
            #
            equips = " / ".join(list_errors)
            str_exclusivo = f"Os seguintes equipamentos possuem conjunto diferente de 'Anafas e Anarede': {equips}."
        else:
            str_exclusivo = "Não foram encontrados equipamentos que possuem conjunto diferente de 'Anafas e Anarede'"
        #
        return str_exclusivo

    def check_exclusives(self):
        """
        Função avançada de converter os dataframes para um único
        """
        df_robras_orig, dic_dfs = self.get_all_siger_dfs()
        str_exclusivo = self.__aux_check_exclusives(dic_dfs)

        return str_exclusivo

    # 02. Estados Múltiplos
    def __aux_check_estados_multiplos(self, df, df_siger):
        """
        Função avançada de converter os dataframes para um único
        """
        condicao = ["Como Construído", "Acesso", "Carga Inicial", "Típico", "Pré-Operacional", "Projeto Básico", "Agente Fora da RB"]
        df = df[~df['Estado'].isin(condicao)]
        df = df[~df["Código de Obra de Entrada"].str.startswith("BASE_")]
        list_obras = df["Código de Obra de Entrada"].to_list()
        df_filtrado = df_siger[df_siger["Código de Obra de Entrada"].isin(list_obras)]
        df_filtrado = df_filtrado.sort_values(by='Código de Obra de Entrada', ascending=False)

        return df_filtrado

    def check_estados_multiplos(self):
        """
        Função avançada de converter os dataframes para um único
        """
        df_siger = self.get_base_siger()
        #
        df_agg = df_siger.groupby(['Código de Obra de Entrada', "Data de Entrada"], as_index=False).agg({'Estado': lambda x: ' '.join(set(x))})
        #
        df_estado_mult = self.__aux_check_estados_multiplos(df_agg, df_siger)

        return df_estado_mult

    # 03. Datas múltiplas
    def __aux_check_datas_multiplas(self, df):
        """
        Função avançada de converter os dataframes para um único
        """
        df = df[df['Código de Obra de Entrada'].duplicated()]
        df = df[~df['Código de Obra de Entrada'].str.startswith('BASE_')]

        return df

    def check_datas_multiplas(self):
        """
        Função avançada de converter os dataframes para um único
        """
        df_siger = self.get_base_siger()
        #
        df_agg = df_siger.groupby(['Código de Obra de Entrada', "Data de Entrada"], as_index=False).agg({'Estado': lambda x: ' '.join(set(x))})
        #
        df_data_mult = self.__aux_check_datas_multiplas(df_agg)

        return df_data_mult

    # 04. Estados Defasados
    def __aux_check_estados_defasados(self, df_agg):
        """
        Função avançada de converter os dataframes para um único
        """
        current_datetime = datetime.datetime.now()
        day = current_datetime.day
        month = current_datetime.month
        year = current_datetime.year
        today = f"{day:02d}-{month:02d}-{year}"
        df_past = df_agg.copy()
        df_past['Data de Entrada'] = pd.to_datetime(df_past['Data de Entrada'])
        df_past = df_past[df_past['Data de Entrada'] < current_datetime]
        df_past = df_past[~df_past["Código de Obra de Entrada"].str.startswith("BASE_")]
        condicao = ["Como Construído", "Pré-Operacional", "Agente Fora da RB"]
        df_past = df_past[~df_past['Estado'].isin(condicao)]
        df_past = df_past.sort_values(by='Data de Entrada')

        return df_past

    def check_estados_defasados(self):
        """
        Função avançada de converter os dataframes para um único
        """
        df_siger = self.get_base_siger()
        #
        df_agg = df_siger.groupby(['Código de Obra de Entrada', "Data de Entrada"], as_index=False).agg({'Estado': lambda x: ' '.join(set(x))})
        #
        df_estado_def = self.__aux_check_estados_defasados(df_agg)

        return df_estado_def

    # 05. Nomes repetidos
    def __aux_check_nome_repetidos(self, df_agg):
        """
        Função avançada de converter os dataframes para um único
        """
        df_bar = df_agg[["Número", "Nome"]]
        df_bar_dup = df_bar[df_bar.duplicated(subset='Nome', keep=False)].sort_values(by='Número')
        df_bar_uniq = df_bar_dup.drop_duplicates(keep=False).sort_values(by='Nome')
        exceptions = ["NIGUT6-RJ000","NIGUT6-RJ013","NIGUT8-RJ000","NIGUT8-RJ013"]
        df_bar_uniq = df_bar_uniq[~df_bar_uniq['Nome'].isin(exceptions)]

        return df_bar_uniq

    def check_nome_repetidos(self):
        """
        Função avançada de converter os dataframes para um único
        """
        df_siger = self.get_base_siger()
        #
        df_agg = df_siger.groupby(['Código de Obra de Entrada', "Data de Entrada"], as_index=False).agg({'Estado': lambda x: ' '.join(set(x))})
        #
        df_nom_rep = self.__aux_check_nome_repetidos(df_agg)

        return df_nom_rep

    # 06. Checagem nos comentários
    def __analisa_comentarios_siger(self, dic_decks):
        # Inicializa dicionário para capturar erros
        dic_erro_coment = {"obras_sem_com_empreendedimento": [], "obras_sem_com_tipo_obra": [], "obras_sem_com_regiao": [],
                           "obras_com_vaz_empreendedimento": [], "obras_com_vaz_tipo_obra": [], "obras_com_vaz_regiao": [],
                           "obras_com_erro_tipo": [], "obras_com_erro_regiao": []}

        # Verificação dos erros
        for index, (codigo_obra, comentario) in enumerate(dic_decks.items()):
            # Verifica se não tem comentário
            if isinstance(comentario,float):
                comentario = ""

            if ("(= EMPREENDIMENTO" not in comentario):
                dic_erro_coment["obras_sem_com_empreendedimento"].append(codigo_obra)

            if ("(= TIPO OBRA" not in comentario):
                dic_erro_coment["obras_sem_com_tipo_obra"].append(codigo_obra)

            if ("(= REGIÃO" not in comentario):
                dic_erro_coment["obras_sem_com_regiao"].append(codigo_obra)

            # Verifica empreendimento
            if ("(= EMPREENDIMENTO:                                                                                               =)" in comentario):
                dic_erro_coment["obras_com_vaz_empreendedimento"].append(codigo_obra)

            # # Verifica região
            if ("(= REGIÃO        :                                                                                               =)" in comentario):
                dic_erro_coment["obras_com_vaz_regiao"].append(codigo_obra)

            # Verifica tipo obra
            if ("(= TIPO OBRA     :                                                                                               =)" in comentario):
                dic_erro_coment["obras_com_vaz_tipo_obra"].append(codigo_obra)

            # Coletando dado inserido no campo Tipo Obra
            if comentario.find("(= TIPO OBRA") > 0:
                start_string = comentario.find("(= TIPO OBRA")
                end_string = comentario.find("\r\n", start_string+2)
                tipo_obra = comentario[start_string+12:end_string-2].replace(":","").strip()

                if tipo_obra not in ["TRANSMISSÃO", "TRANSMISSÃO (DIT)", "CONSUMIDOR", "GERAÇÃO - UHE","GERAÇÃO - UTE","GERAÇÃO - UEE","GERAÇÃO - UFV","GERAÇÃO - PCH","DISTRIBUIÇÃO COM IMPACTO SISTÊMICO"]:
                    dic_erro_coment["obras_com_erro_tipo"].append(codigo_obra)

            # Coletando dado inserido no campo Região
            if comentario.find("(= REGIÃO        :") > 0:
                start_string = comentario[comentario.find("(= REGIÃO        :"):]
                end_string = start_string[:start_string.find("\n")].strip()
                regiao = (end_string.replace("(= REGIÃO        :","")).replace("=)","").strip()
                if regiao not in ["S+MS","SECO","NNE"]:
                    dic_erro_coment["obras_com_erro_regiao"].append(codigo_obra)

        return dic_erro_coment

    def __aux_check_comentarios(self, df_robras):
        # Coletando dicionário com erros nos comentários
        # df_robras = oSIGER.get_robras()
        df_robras['Data'] = pd.to_datetime(df_robras['Data'], format='%d/%m/%Y')
        df_robras = df_robras[df_robras['Data'] >= '2023-10-01']
        dic_decks = df_robras.set_index('Código de Obra')['Comentário sobre a Obra'].to_dict()
        #
        dic_erro_coment = self.__analisa_comentarios_siger(dic_decks)

        # Imprimindo na tela os resultados
        list_report = []
        list_report.append("Análise sobre o campo COMENTÁRIO presente no servidor siger selecionado:\n")
        list_report.append(f"Foram analisados {len(dic_decks)} códigos de obra presentes no servidor, com data de entrada igual ou superior a 01/10/2023. \nSeguem resultados: \n")
        len_errors = sum(len(lst) for lst in dic_erro_coment.values())

        if len_errors == 0:
            list_report.append("- Análise concluída com sucesso sem erros aparentes!")
        else:
            if len(dic_erro_coment["obras_sem_com_empreendedimento"]) > 0:
                list_report.append("- Verificar falta das informações de 'EMPREENDIMENTO' do cabeçalho padrão dos seguintes códigos de obra:")
                list_report.append("\n".join(dic_erro_coment["obras_sem_com_empreendedimento"]))
                list_report.append("\n")
            if len(dic_erro_coment["obras_sem_com_regiao"]) > 0:
                list_report.append("- Verificar falta das informações de 'REGIÃO' do cabeçalho padrão dos seguintes códigos de obra:")
                list_report.append("\n".join(dic_erro_coment["obras_sem_com_regiao"]))
                list_report.append("\n")
            if len(dic_erro_coment["obras_sem_com_tipo_obra"]) > 0:
                list_report.append("- Verificar falta das informações de 'TIPO OBRA' do cabeçalho padrão dos seguintes códigos de obra:")
                list_report.append("\n".join(dic_erro_coment["obras_sem_com_tipo_obra"]))
                list_report.append("\n")
            if len(dic_erro_coment["obras_com_vaz_empreendedimento"]) > 0:
                list_report.append("- Verificar falta de preenchimento do campo COMENTÁRIO - EMPREENDIMENTO dos seguintes códigos de obra:")
                list_report.append("\n".join(dic_erro_coment["obras_com_vaz_empreendedimento"]))
                list_report.append("\n")
            if len(dic_erro_coment["obras_com_vaz_tipo_obra"]) > 0:
                list_report.append("- Verificar falta de preenchimento do campo COMENTÁRIO - TIPO OBRA dos seguintes códigos de obra:")
                list_report.append("\n".join(dic_erro_coment["obras_com_vaz_tipo_obra"]))
                list_report.append("\n")
            if len(dic_erro_coment["obras_com_vaz_regiao"]) > 0:
                list_report.append("- Verificar falta de preenchimento do campo COMENTÁRIO - REGIÃO dos seguintes códigos de obra:")
                list_report.append("\n".join(dic_erro_coment["obras_com_vaz_regiao"]))
                list_report.append("\n")
            if len(dic_erro_coment["obras_com_erro_tipo"]) > 0:
                list_report.append("- Verificar erro de preenchimento no campo TIPO OBRA dos seguintes códigos de obra. Lembrando que são apenas válidos os seguintes valores ['TRANSMISSÃO','GERAÇÃO - UHE','GERAÇÃO - UTE','GERAÇÃO - UEE','GERAÇÃO - UFV','GERAÇÃO - PCH','DISTRIBUIÇÃO COM IMPACTO SISTÊMICO']:")
                list_report.append("\n".join(dic_erro_coment["obras_com_erro_tipo"]))
                list_report.append("\n")
            if len(dic_erro_coment["obras_com_erro_regiao"]) > 0:
                list_report.append("- Verificar erro de preenchimento no campo REGIÃO dos seguintes códigos de obra. Lembrando que são apenas válidos os seguintes valores ['S+MS','SECO','NNE']:")
                list_report.append("\n".join(dic_erro_coment["obras_com_erro_regiao"]))
                list_report.append("\n")

        return "\n".join(list_report)


        """
        Função avançada de converter os dataframes para um único
        """
        df_robras_orig, dic_dfs = self.get_all_siger_dfs()
        str_exclusivo = self.__aux_check_exclusives(dic_dfs)

        return str_exclusivo

    def check_comentarios(self):
        """
        Função avançada de converter os dataframes para um único
        """
        df_robras_mod, dic_dfs = self.get_all_siger_dfs()

        str_comentarios = self.__aux_check_comentarios(df_robras_mod)

        return str_comentarios

    # 07. Verifica escorregamento em cascata
    def __check_change_date(self, data_antes, data_depois):
        if data_antes == data_depois:
            id = "N"
        else:
            id = "S"
        return id

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

    # 08. Verifica apagamento em cascata
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

    # 09. Verifica obras não presentes no banco, mas que estavam no 5 e 6
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

    ###================================================================================================================
    ###
    ### VERIFICAÇÃO GERAL PÓS CARREGAMENTO
    ###
    ###================================================================================================================
    def verifica_carregamento(self, path_decks="", df_robras_original = ""): #carrega_7_arquivos_gui_pt2
        """ Analisa o carregamento automático dos 7 arquivos"""
        # Finalizada a execução do carregamento, verificar o resultado obtido
        df_robras_mod, dic_dfs = self.get_all_siger_dfs()
        df_siger = self._make_siger_base(dic_dfs)
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

        # PARTE 5 - CHECAR NOMES DE BARRAS REPETIDAS
        df_barra_nome_repet = self.__aux_check_nome_repetidos(dic_dfs["barra"])

        # PARTE 6 - CHECAGEM COMENTÁRIOS
        str_comentarios = self.__aux_check_comentarios(df_robras_mod)

        # Crie um arquivo de texto para escrever o relatório
        report = []
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report.append("\n" + "#"*88 + "\n")
        report.append(f"# RELATÓRIO DE CARREGAMENTO SIGER - {data_hora}\n\n")

        # Escreva a variável string no arquivo
        report.append("#"*88 + "\n")
        report.append("# CHECAGEM 01 - CONJUNTOS EXCLUSIVOS\n")
        report.append(f"{str_exclusivo}\n\n")

        # Escreva os DataFrames no arquivo
        report.append("#"*88 + "\n")
        report.append("# CHECAGEM 02 - ESTADOS MÚLTIPLOS\n")
        df_estado_mult_mod = df_estado_mult.copy()
        df_estado_mult_mod['Data de Entrada'] = pd.to_datetime(df_estado_mult_mod['Data de Entrada']).dt.strftime('%d/%m/%Y')
        df_estado_mult_mod['Data de Saída'] = pd.to_datetime(df_estado_mult_mod['Data de Saída']).dt.strftime('%d/%m/%Y')
        if len(df_estado_mult_mod) > 0:
            report.append(df_estado_mult_mod.to_string(index=False) + '\n\n')
        else:
            report.append(" NÃO FORAM ENCONTRADAS OBRAS COM ESTADOS MÚLTIPLOS!\n")

        report.append("#"*88 + "\n")
        report.append("# CHECAGEM 03 - DATAS MÚLTIPLAS\n")
        df_data_mult_mod = df_data_mult.copy()
        df_data_mult_mod['Data de Entrada'] = pd.to_datetime(df_data_mult_mod['Data de Entrada']).dt.strftime('%d/%m/%Y')
        if len(df_data_mult_mod) > 0:
            report.append(df_data_mult_mod.to_string(index=False) + '\n\n')
        else:
            report.append(" NÃO FORAM ENCONTRADAS OBRAS COM DATAS MÚLTIPLAS!\n")

        report.append("#"*88 + "\n")
        report.append("# CHECAGEM 04 - ESTADOS DEFASADOS\n")
        df_estado_def_mod = df_estado_def.copy()
        df_estado_def_mod['Data de Entrada'] = pd.to_datetime(df_estado_def_mod['Data de Entrada']).dt.strftime('%d/%m/%Y')
        if len(df_estado_def_mod) > 0:
            report.append(df_estado_def_mod.to_string(index=False) + '\n\n')
        else:
            report.append(" NÃO FORAM ENCONTRADAS OBRAS COM ESTADOS DEFASADOS!\n")

        report.append("#"*88 + "\n")
        report.append("# CHECAGEM 05 - BARRAS COM NOMES REPETIDOS\n")
        df_barra_nome_repet_mod = df_barra_nome_repet.copy()
        if len(df_barra_nome_repet_mod) > 0:
            report.append(df_barra_nome_repet_mod.to_string(index=False) + '\n\n')
        else:
            report.append(" NÃO FORAM ENCONTRADAS BARRAS COM NOMES REPETIDOS!\n")

        report.append("#"*88 + "\n")
        report.append("# CHECAGEM 06 - PREENCHIMENTO COMENTÁRIOS\n")
        report.append(f"{str_comentarios}\n\n")

        # Coleta lista de decks presentes na pasta
        if path_decks != "":
            decks_siger = []
            for filename in os.listdir(path_decks):
                if filename.endswith(('.pwf', '.alt')) or filename.startswith(('1_', '2_', '3_', '4_', '5_', '6_', '7_')):
                    decks_siger.append(os.path.join(path_decks, filename))

            # Verifica se estamos com os 7 arquivos para conseguir prosseguir:
            if len(decks_siger) == 7:
                # PARTE 5 - VERIFICAR ESCORREGAMENTOS EM CASCATA
                df_obras_escorregadas_cascata = self.check_escorreg_cascata(df_robras_original, df_robras_mod, decks_siger[6])
                #
                # PARTE 6 - VERIFICAR EXCLUSÕES EM CASCATA
                lista_obras_removidas_cascata = self.check_apagamento_cascata(df_robras_original, df_robras_mod, decks_siger[0], decks_siger[3])

                # PARTE 7 - VERIFICAR FALSAS INCLUSÕES NA BASE
                lista_obras_falso_positivo = self.check_obras_nao_presentes(df_robras_mod, decks_siger[4], decks_siger[5])

                report.append("#"*88 + "\n")
                report.append("# CHECAGEM 07 - OBRAS ESCORREGADAS EM CASCATA\n")
                df_obras_escorregadas_cascata_mod = df_obras_escorregadas_cascata.copy()
                df_obras_escorregadas_cascata_mod['Data_antes'] = pd.to_datetime(df_obras_escorregadas_cascata_mod['Data_antes']).dt.strftime('%d/%m/%Y')
                df_obras_escorregadas_cascata_mod['Data_depois'] = pd.to_datetime(df_obras_escorregadas_cascata_mod['Data_depois']).dt.strftime('%d/%m/%Y')
                df_obras_escorregadas_cascata_mod['Data_Arquivo_7'] = pd.to_datetime(df_obras_escorregadas_cascata_mod['Data_Arquivo_7']).dt.strftime('%d/%m/%Y')
                if len(df_obras_escorregadas_cascata_mod) > 0:
                    report.append(df_obras_escorregadas_cascata_mod.to_string(index=False) + '\n\n')
                else:
                    report.append(" NÃO FORAM ENCONTRADAS OBRAS ESCORREGADAS EM CASCATA!\n")

                report.append("#"*88 + "\n")
                report.append("# CHECAGEM 08 - OBRAS APAGADAS EM CASCATA\n")
                if len(lista_obras_removidas_cascata) > 0:
                    report.append("\n".join(lista_obras_removidas_cascata) + '\n\n')
                else:
                    report.append(" NÃO FORAM ENCONTRADAS OBRAS APAGADAS EM CASCATA!\n")

                report.append("#"*88 + "\n")
                report.append("# CHECAGEM 09 - OBRAS PRESENTES NOS ARQUIVOS 5/6 MAS NÃO INCLUÍDAS NO BANCO\n")
                if len(lista_obras_falso_positivo) > 0:
                    report.append("\n".join(lista_obras_falso_positivo) + '\n\n')
                else:
                    report.append(" NÃO FORAM ENCONTRADAS OBRAS PRESENTES NOS ARQUIVOS 5/6 MAS NÃO INCLUÍDAS NO BANCO!\n")
            else:
                print("Não foi possível localizar os 7 arquivos na pasta informada! Favor conferir se os decks estão na pasta ou se há mais decks que os 7 a serem analisados!")

        str_report = "\n".join(report)
        return str_report

    ###================================================================================================================
    ###
    ### CÓDIGOS PARA AUXÍLIO NA VISUALIZAÇÃO DO ESCORREGAMENTO
    ###
    ###================================================================================================================
    def __get_dados_lt(self, row):
        barra_de = (row["ID"].split("#"))[1]
        barra_de = "#"+barra_de+"#"
        barra_pa = (row["ID"].split("#"))[3]
        barra_pa = "#"+barra_pa+"#"
        num_circ = (row["ID"].split("$"))[1]
        circ1 = barra_de + "-" + barra_pa + "-$" + num_circ + "$"
        circ2 = barra_pa + "-" + barra_de + "-$" + num_circ + "$"

        return barra_de, barra_pa, num_circ, circ1, circ2

    def __get_dados_lt_2(self, row):
        barra_de = (row["ID"].split("#"))[5]
        barra_de = "#"+barra_de+"#"
        barra_pa = (row["ID"].split("#"))[7]
        barra_pa = "#"+barra_pa+"#"
        num_circ = (row["ID"].split("$"))[7]
        circ1 = barra_de + "-" + barra_pa + "-$" + num_circ + "$"
        circ2 = barra_pa + "-" + barra_de + "-$" + num_circ + "$"

        return barra_de, barra_pa, num_circ, circ1, circ2

    def __dependentes_futuros(self, df_siger, row, tipo):
        # Filtro de tipo de eqps
        df_temp = df_siger.copy()
        #
        if tipo == "BR":
            barra_de = "#" + (row["ID"].split("#"))[1] + "#"
            df_temp = df_temp[df_temp['ID'].str.contains(barra_de)]
        elif tipo == "CR":
            df_temp = df_temp[df_temp['ID'] == row["ID"]]
        elif tipo == "CS":
            df_temp = df_temp[df_temp['ID'] == row["ID"]]
        elif tipo == "LT":
            _, _, _, circ1, circ2 = self.__get_dados_lt(row)
            df_temp = df_temp[df_temp['ID'].str.contains(circ1,regex=False) | df_temp['ID'].str.contains(circ2,regex=False)]
        elif tipo == "MT":
            df_temp = df_temp[df_temp['ID'] == row["ID"]]
        elif tipo == "SB":
            df_temp = df_temp[df_temp['ID'] == row["ID"]]
        elif tipo == "SL":
            df_temp = df_temp[df_temp['ID'] == row["ID"]]
        elif tipo == "TR":
            _, _, _, circ1, circ2 = self.__get_dados_lt(row)
            df_temp = df_temp[df_temp['ID'].str.contains(circ1,regex=False) | df_temp['ID'].str.contains(circ2,regex=False)]

        # Removendo código de obra de entrada atual e saída.....quero somente dependentes indiretos...
        df_temp= df_temp[df_temp['Código de Obra de Entrada'] != row["Código de Obra de Entrada"]]
        df_temp= df_temp[df_temp['Código de Obra de Saída'] != row["Código de Obra de Entrada"]]

        # Garantindo que são obras pais que já existiam antes da entrada desse equipamento
        df_temp = df_temp[df_temp['Data de Entrada'] >= row["Data de Entrada"]]
        # df_temp = df_temp[df_temp['Data de Entrada'] <= row["Data de Saída"]]

        if not df_temp.empty:
            pass

        return df_temp

    def __dependentes_passados(self, df_siger, row, tipo):
        # Filtro de tipo de eqps
        df_temp = df_siger.copy()
        #
        if tipo == "BR":
            df_temp = df_temp[df_temp['ID'] == row["ID"]]
        elif tipo == "CR":
            barra_de = "#" + (row["ID"].split("#"))[1] + "#"
            #
            df_temp1 = df_temp[df_temp['ID'].str.contains(barra_de,regex=False)]
            df_temp1 = df_temp1[(df_temp1['Tipo'] == "BR")]
            #
            df_temp2 = df_temp[df_temp['ID'] == row["ID"]]
            #
            df_temp = pd.concat([df_temp1, df_temp2])
        elif tipo == "CS":
            barra_de, barra_pa, numcirc, circ1, circ2 = self.__get_dados_lt(row)
            #
            df_temp1 = df_temp[df_temp['ID'].str.contains(circ1,regex=False) | df_temp['ID'].str.contains(circ2,regex=False)]
            df_temp1 = df_temp1[(df_temp1['Tipo'] == "LT")]
            #
            df_temp2 = df_temp[df_temp['ID'].str.contains(barra_de,regex=False) | df_temp['ID'].str.contains(barra_pa,regex=False)]
            df_temp2 = df_temp2[(df_temp2['Tipo'] == "BR")]
            #
            df_temp3 = df_temp[df_temp['ID'] == row["ID"]]
            #
            df_temp = pd.concat([df_temp1, df_temp2, df_temp3])
        elif tipo == "LT":
            barra_de, barra_pa, numcirc, circ1, circ2 = self.__get_dados_lt(row)
            #
            df_temp1 = df_temp[df_temp['ID'].str.contains(circ1,regex=False) | df_temp['ID'].str.contains(circ2,regex=False)]
            df_temp1 = df_temp1[(df_temp1['Tipo'] == "LT")]
            #
            df_temp2 = df_temp[df_temp['ID'].str.contains(barra_de,regex=False) | df_temp['ID'].str.contains(barra_pa,regex=False)]
            df_temp2 = df_temp2[(df_temp2['Tipo'] == "BR")]
            #
            df_temp = pd.concat([df_temp1, df_temp2])

        elif tipo == "MT":
            barra_de1, barra_pa1, numcirc1, circ1, circ2 = self.__get_dados_lt(row)
            barra_de2, barra_pa2, numcirc2, circ3, circ4 = self.__get_dados_lt_2(row)
            #
            df_temp1 = df_temp[df_temp['ID'].str.contains(barra_de1,regex=False) | df_temp['ID'].str.contains(barra_pa1,regex=False) | df_temp['ID'].str.contains(barra_de2,regex=False) | df_temp['ID'].str.contains(barra_pa2,regex=False)]
            df_temp1 = df_temp1[(df_temp1['Tipo'] == "BR")]
            #
            df_temp2 = df_temp[df_temp['ID'].str.contains(circ1,regex=False) | df_temp['ID'].str.contains(circ2,regex=False) | df_temp['ID'].str.contains(circ3,regex=False) | df_temp['ID'].str.contains(circ4,regex=False)]
            df_temp2 = df_temp2[(df_temp2['Tipo'] == "LT")]
            #
            df_temp3 = df_temp[df_temp['ID'] == row["ID"]]
            #
            df_temp = pd.concat([df_temp1, df_temp2, df_temp3])

        elif tipo == "SB":
            barra_de = "#" + (row["ID"].split("#"))[1] + "#"
            #
            df_temp1 = df_temp[df_temp['ID'].str.contains(barra_de,regex=False)]
            df_temp1 = df_temp1[(df_temp1['Tipo'] == "BR")]
            #
            df_temp2 = df_temp[df_temp['ID'] == row["ID"]]
            #
            df_temp = pd.concat([df_temp1, df_temp2])

        elif tipo == "SL":
            barra_de, barra_pa, numcirc, circ1, circ2 = self.__get_dados_lt(row)
            #
            df_temp1 = df_temp[df_temp['ID'].str.contains(circ1,regex=False) | df_temp['ID'].str.contains(circ2,regex=False)]
            df_temp1 = df_temp1[(df_temp1['Tipo'] == "LT")]
            #
            df_temp2 = df_temp[df_temp['ID'].str.contains(barra_de,regex=False) | df_temp['ID'].str.contains(barra_pa,regex=False)]
            df_temp2 = df_temp2[(df_temp2['Tipo'] == "BR")]
            #
            df_temp3 = df_temp[df_temp['ID'] == row["ID"]]
            #
            df_temp = pd.concat([df_temp1, df_temp2, df_temp3])

        elif tipo == "TR":
            barra_de, barra_pa, numcirc, circ1, circ2 = self.__get_dados_lt(row)
            #
            df_temp1 = df_temp[df_temp['ID'].str.contains(circ1,regex=False) | df_temp['ID'].str.contains(circ2,regex=False)]
            df_temp1 = df_temp1[(df_temp1['Tipo'] == "TR")]
            #
            df_temp2 = df_temp[df_temp['ID'].str.contains(barra_de,regex=False) | df_temp['ID'].str.contains(barra_pa,regex=False)]
            df_temp2 = df_temp2[(df_temp2['Tipo'] == "BR")]
            #
            df_temp = pd.concat([df_temp1, df_temp2])

        # Removendo código de obra de entrada atual e saída.....quero somente dependentes indiretos...
        df_temp= df_temp[df_temp['Código de Obra de Entrada'] != row["Código de Obra de Entrada"]]
        df_temp= df_temp[df_temp['Código de Obra de Saída'] != row["Código de Obra de Entrada"]]

        # Garantindo que são obras pais que já existiam antes da entrada desse equipamento
        df_temp = df_temp[df_temp['Data de Entrada'] <= row["Data de Entrada"]]
        # df_temp = df_temp[df_temp['Data de Entrada'] <= row["Data de Saída"]]

        if not df_temp.empty:
            pass

        return df_temp

    def get_dependancies(self, df_siger, df_obra):
        """
        # Todos os equipamentos aqui relacionados portanto nascem no mesmo código de obra [A] na data de entrada [I]
        #
        # A ideia do escorregamento é mudar a data de entrada [I] para [II], que pode ser anterior ou posterior
        #
        # Portanto, a ideia é considerar essa obra como "pai" e buscar todos os possíveis "filhos" dessas obras, assim, eu descubro
        # todas as obras dependentes dessa obra. O esquema de paternidade pode ser resumido da seguinte forma
        #  __________________________________________________________________________________________________________________
        # I-- TIPO EQP -- I -- TIPO DE EQP DE OBRAS DEPENDENTES -- I -- CONDIÇÃO DE DATA -- I -- CONDIÇÃO DE CÓDIGO DE OBRA --I
        # I-------------------------------------------------------------------------------------------------------------------I
        # IBR             I BR / CR / CS / LT / MT / SB / SL / TR  I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        # I-------------------------------------------------------------------------------------------------------------------I
        # ICR             I CR                                     I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        # I-------------------------------------------------------------------------------------------------------------------I
        # ICS             I CS                                     I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        # I-------------------------------------------------------------------------------------------------------------------I
        # ILT             I CS / LT / MT / SL                      I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        # I-------------------------------------------------------------------------------------------------------------------I
        # IMT             I MT                                     I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        # I-------------------------------------------------------------------------------------------------------------------I
        # ISB             I SB                                     I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        # I-------------------------------------------------------------------------------------------------------------------I
        # ISL             I SL                                     I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        # I-------------------------------------------------------------------------------------------------------------------I
        # ITR             I TR                                     I MAIOR QUE [I]          I DIFERENTE DE [A]                I
        # I___________________________________________________________________________________________________________________I
        """
        # Essa vai ser o núcleo da busca do relatório de dependentes dessa obra - EM PRIMEIRO NÍVEL
        df_dependentes_futuro = pd.DataFrame()
        df_dependentes_passado = pd.DataFrame()
        data_entrada_depend_futuro = ""
        idx_data_futuro = ""
        data_entrada_depend_passado = ""
        idx_data_passado = ""

        for index, row in df_obra.iterrows():
            # Vou preencher o df_temp com obras dependentes do eqp da df_obra analisado
            # Os dados de ROW são da obra pai / os dados de df_temp são das obras dependentes
            df_temp = pd.DataFrame()
            match row["Tipo"]:
                case "BR":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "BR")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "BR")
                case "CR":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "CR")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "CR")
                case "CS":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "CS")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "CS")
                case "LT":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "LT")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "LT")
                case "MT":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "MT")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "MT")
                case "SB":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "SB")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "SB")
                case "SL":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "SL")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "SL")
                case "TR":
                    df_temp_futuro = self.__dependentes_futuros(df_siger, row, "TR")
                    df_temp_passado = self.__dependentes_passados(df_siger, row, "TR")
            # Encontrando alguma obra dependente no horizonte futuro
            if not df_temp_futuro.empty:
                df_temp = df_temp_futuro.copy()
                df_temp = df_temp.assign(Tipo_PAI=row["Tipo"])
                df_temp = df_temp.assign(ID_PAI=row["ID"])
                df_temp = df_temp.assign(CO_Entrada_PAI=row["Código de Obra de Entrada"])
                df_temp = df_temp.assign(Data_Entrada_PAI=row["Data de Entrada"])
                #
                df_dependentes_futuro = pd.concat([df_dependentes_futuro, df_temp], ignore_index=True)
                data_entrada_depend_futuro = min(df_dependentes_futuro["Data de Entrada"])
                idx_data_futuro = pd.to_datetime(df_dependentes_futuro["Data de Entrada"]).idxmin()
                #
                df_dependentes_futuro = df_dependentes_futuro.sort_values(by='Data de Entrada', ascending=True)

            # Encontrando alguma obra dependente no horizonte passado
            if not df_temp_passado.empty:
                df_temp = df_temp_passado.copy()
                df_temp = df_temp.assign(Tipo_FILHO=row["Tipo"])
                df_temp = df_temp.assign(ID_FILHO=row["ID"])
                df_temp = df_temp.assign(CO_Entrada_FILHO=row["Código de Obra de Entrada"])
                df_temp = df_temp.assign(Data_Entrada_FILHO=row["Data de Entrada"])
                #
                df_dependentes_passado = pd.concat([df_dependentes_passado, df_temp], ignore_index=True)
                data_entrada_depend_passado = max(df_dependentes_passado["Data de Entrada"])
                idx_data_passado = pd.to_datetime(df_dependentes_passado["Data de Entrada"]).idxmax()
                #
                df_dependentes_passado = df_dependentes_passado.sort_values(by='Data de Entrada', ascending=True)

        return data_entrada_depend_futuro, idx_data_futuro, df_dependentes_futuro, data_entrada_depend_passado, idx_data_passado, df_dependentes_passado

    def visualiza_obra(self, df_siger, codigo_obra_vis):
        # Obtendo o dataframe de com equipamentos
        df_siger_principal = df_siger[(df_siger["Código de Obra de Entrada"] == codigo_obra_vis)
                                      |
                                      (df_siger["Código de Obra de Saída"] == codigo_obra_vis)]
        df_siger_principal_ent = df_siger[(df_siger["Código de Obra de Entrada"] == codigo_obra_vis)]

        # Obtendo dados dos dependentes
        if not df_siger_principal_ent.empty:
            data_dep_futuro, idx_futuro, df_dependentes_futuro, data_dep_passado, idx_passado, df_dependentes_passado = self.get_dependancies(df_siger, df_siger_principal_ent)
        else:
            data_dep_futuro, idx_futuro, df_dependentes_futuro, data_dep_passado, idx_passado, df_dependentes_passado = "","","","","",""

        # Ajuste data
        df_siger['Data de Entrada'] = pd.to_datetime(df_siger['Data de Entrada']).dt.strftime('%d/%m/%Y')
        df_siger['Data de Saída'] = pd.to_datetime(df_siger['Data de Saída']).dt.strftime('%d/%m/%Y')

        # Inserções
        df_siger_principal_in = df_siger[(df_siger["Código de Obra de Entrada"] == codigo_obra_vis)]
        data_in = df_siger_principal_in["Data de Entrada"].iloc[0]
        df_temp = df_siger_principal_in.dropna(subset = ["Data de Saída"])
        if len(df_temp) > 0:
            df_temp = df_temp.sort_values(by=['Data de Saída', 'Código de Obra de Saída'], ascending=True)
            data_out = df_temp["Data de Saída"].iloc[0]
        else:
            data_out = ""

        # Obras dependentes que devem existir na base
        if len(df_dependentes_passado) > 0:
            df_dependentes_passado_visualiz = df_dependentes_passado[['Tipo','ID','Código de Obra de Entrada','Código de Obra de Saída','Data de Entrada','Data de Saída','ID_FILHO']].copy()
            df_dependentes_passado_visualiz.loc[:,'Data de Entrada'] = pd.to_datetime(df_dependentes_passado_visualiz['Data de Entrada']).dt.strftime('%d/%m/%Y')
            df_dependentes_passado_visualiz.loc[:,'Data de Saída'] = pd.to_datetime(df_dependentes_passado_visualiz['Data de Saída']).dt.strftime('%d/%m/%Y')
            # Obras dependentes fora do BAS_JUN20
            df_dependentes_passado_visualiz = df_dependentes_passado_visualiz[
                                                    ~((df_dependentes_passado_visualiz["Código de Obra de Entrada"] == "BASE_JUN20")
                                                    &
                                                    (df_dependentes_passado_visualiz["Código de Obra de Saída"].isna()))]
        else:
            df_dependentes_passado_visualiz = pd.DataFrame()

        if len(df_dependentes_futuro) > 0:
            # Obras dependentes que irão existir na base
            df_dependentes_futuro_visualiz = df_dependentes_futuro[['Tipo','ID','Código de Obra de Entrada','Código de Obra de Saída','Data de Entrada','Data de Saída','ID_PAI']]
            df_dependentes_futuro_visualiz['Data de Entrada'] = pd.to_datetime(df_dependentes_futuro_visualiz['Data de Entrada']).dt.strftime('%d/%m/%Y')
            df_dependentes_futuro_visualiz['Data de Saída'] = pd.to_datetime(df_dependentes_futuro_visualiz['Data de Saída']).dt.strftime('%d/%m/%Y')
            # Obras dependentes fora do BAS_JUN20
            df_dependentes_futuro_visualiz = df_dependentes_futuro_visualiz[
                                                    ~((df_dependentes_futuro_visualiz["Código de Obra de Entrada"] == "BASE_JUN20")
                                                    &
                                                    (df_dependentes_futuro_visualiz["Código de Obra de Saída"].isna()))]
        else:
            df_dependentes_futuro_visualiz = pd.DataFrame()

        # Exclusões
        df_siger_principal_out = df_siger[(df_siger["Código de Obra de Saída"] == codigo_obra_vis)]

        # Montando relatório
        list_report = []
        list_report.append(f"\nANÁLISE DOS EQUIPAMENTOS E DEPENDÊNCIAS DA OBRA : {codigo_obra_vis}\n")

        # Apresentando a obra de entrada
        list_report.append("#"*88 + "\nEQUIPAMENTOS A SEREM INTEGRADOS\n")
        if len(df_siger_principal_in) > 0:
            list_report.append(f"O código de obra {codigo_obra_vis} irá integrar no SIGER os seguintes equipamentos:\n")
            df_siger_principal_in.loc[:, 'ID'] = df_siger_principal_in['ID'].str.replace('[#$]', '', regex=True)
            list_report.append(df_siger_principal_in.fillna('-').to_string(index=False) + '\n\n')
        else:
            list_report.append(f"O código de obra {codigo_obra_vis} não integra no SIGER novos equipamentos.\n")

        # Apresentando a obra de entrada
        list_report.append("#"*88 + "\nEQUIPAMENTOS A SEREM INTEGRADOS - DEPENDÊNCIA PASSADA\n")
        if len(df_dependentes_passado_visualiz) > 0:
            list_report.append(f"Para que o código de obra {codigo_obra_vis} seja integrado corretamente no SIGER, os seguintes equipamentos DEVEM EXISTIR ANTES da integração dessa obra no banco:")
            list_report.append(f"***DICA: Se alguma dessas obras for escorregada para uma data futura da data de entrada atual ({data_in}), irá levar de reboque a obra {codigo_obra_vis} para esta data!\n")
            df_dependentes_passado_visualiz.loc[:,'ID'] = df_dependentes_passado_visualiz['ID'].str.replace('[#$]', '', regex=True)
            df_dependentes_passado_visualiz.loc[:,'ID_FILHO'] = df_dependentes_passado_visualiz['ID_FILHO'].str.replace('[#$]', '', regex=True)
            list_report.append(df_dependentes_passado_visualiz.fillna('-').to_string(index=False) + '\n\n')
        else:
            list_report.append(f"O código de obra {codigo_obra_vis} não possui dependências que exigem que equipamentos existam na BASE ANTES da sua integração.\n")

        # Apresentando a obra de saída
        list_report.append("#"*88 + "\nEQUIPAMENTOS A SEREM INTEGRADOS - DEPENDÊNCIA FUTURA\n")
        if len(df_dependentes_futuro_visualiz) > 0:
            list_report.append(f"Para que o código de obra {codigo_obra_vis} seja integrado corretamente no SIGER, os seguintes equipamentos DEVEM EXISTIR DEPOIS da integração dessa obra no banco:")
            list_report.append(f"***DICA: Se alguma dessas obras for escorregada para uma data anterior da data de entrada atual ({data_in}), irá levar de reboque a obra {codigo_obra_vis} para esta data!\n")
            df_dependentes_futuro_visualiz.loc[:,'ID'] = df_dependentes_futuro_visualiz['ID'].str.replace('[#$]', '', regex=True)
            df_dependentes_futuro_visualiz.loc[:,'ID_PAI'] = df_dependentes_futuro_visualiz['ID_PAI'].str.replace('[#$]', '', regex=True)
            list_report.append(df_dependentes_futuro_visualiz.fillna('-').to_string(index=False) + '\n\n')
        else:
            list_report.append(f"O código de obra {codigo_obra_vis} não possui dependências que exigem que equipamentos existam na BASE APÓS a sua integração.\n")

        # Apresentando a obra de exclusão
        list_report.append("#"*88 + "\nEQUIPAMENTOS A SEREM EXCLUÍDOS\n")
        if len(df_siger_principal_out):
            list_report.append(f"Os seguintes equipamentos são excluídos com a integração da obra {codigo_obra_vis} no banco:\n")
            df_siger_principal_out.loc[:,'ID'] = df_siger_principal_out['ID'].str.replace('[#$]', '', regex=True)
            list_report.append(df_siger_principal_out.fillna('-').to_string(index=False) + '\n\n')
        else:
            list_report.append(f"O código de obra {codigo_obra_vis} não exclui nenhum equipamento do banco.\n")

        return list_report
