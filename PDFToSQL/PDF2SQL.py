# pip install jpype tabula openpyxl 
# Dica: Expotar para excel e visualizar a estrutura, caso não esteja correta tentar os parâmetros latice e guess como true/false, cobinações diversas separadamente ou ambos

import os
import tabula
import pandas
from datetime import datetime

def formatar_tipo_beneficio(codigo):
    match codigo:
        case '0':
            return 'NaoIncidencia'
        case '1':
            return 'Isencao'
        case '2':
            return 'ReducaoBaseCalculo'
        case '3':
            return 'Diferimento'
        case '4':
           return 'Suspensao'
        case '5':
            return 'CreditoPresumido'
        

def formatar_sim_ou_nao(valor_comparar):
    match valor_comparar:
        case 'Sim' | 'SIM' | 's' | 'S':
            return 'Sim'
        case _:
            return 'Nao'
        
        
def formatar_data(data_float):
    data_string = ''

    if pandas.isna(data_float):
        data_string = 'null'
    elif len(data_float) == 8:
        data = datetime.strptime(data_float, '%d/%m/%y')
        data_string = f"'{data.strftime('%Y-%m-%d')}'"
    elif len(data_float) == 10:
        data = datetime.strptime(data_float, '%d/%m/%Y')
        data_string = f"'{data.strftime('%Y-%m-%d')}'"
    else:
        raise Exception(f"Tipo de data não tratado: {data_float}")

    return data_string

def gerar_comando_sql_insert(codigo_beneficio, descricao, tipo_beneficio, uf, cst00, cst10, cst20, cst30, cst40, cst41, cst50, cst51, cst53, cst60, cst70, cst90, data_inicial, data_final):
    descricao = descricao.replace('\n', ' ').replace('\r', ' ')
    return f"INSERT INTO EscritaFiscal.BeneficioFiscal (CodBeneficioFiscal, Descricao, TipoBeneficio, UF, CST00, CST10, CST20, CST30, CST40, CST41, CST50, CST51, CST53, CST60, CST70, CST90, DataInicial, DataFinal) VALUES ('{codigo_beneficio}', '{descricao}', '{tipo_beneficio}', '{uf}', '{cst00}', '{cst10}', '{cst20}', '{cst30}', '{cst40}', '{cst41}', '{cst50}', '{cst51}', '{cst53}', '{cst60}', '{cst70}', '{cst90}', {data_inicial}, {data_final});" + '\n\n'
    

def alterar_extencao(nome_arquivo, nova_extensao):
    nome_base, extencao = os.path.splitext(nome_arquivo)
    return nome_base + nova_extensao


def salvar_texto(texto, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.writelines(texto)
        arquivo.close

    print(f"Registros exportados: {len(texto)}")


def importar_tabela_santa_catarina(arquivo_pdf):

    lista_tabela = tabula.read_pdf(arquivo_pdf, pages="all", lattice=True)
    lista_sql = []

    #lista_tabela[0].to_excel(alterar_extencao(arquivo_pdf, '.xlsx'), index=False)

    for tabela in lista_tabela:
        for linha in range(len(tabela)):
            codigo_beneficio = tabela['Código do benefício fiscal'].iloc[linha]
            descricao = tabela['Descrição'].iloc[linha]
            legislacao = f" Legislação {tabela['Legislação'].iloc[linha]}" 
            descricao = descricao + legislacao
            uf = codigo_beneficio[:2]
            data_inicio = formatar_data(tabela['Vigência Início'].iloc[linha])
            data_fim = formatar_data(tabela['Vigência Fim'].iloc[linha])
            tipo_beneficio = formatar_tipo_beneficio(codigo_beneficio[3:-4])
            cst00 = formatar_sim_ou_nao(tabela['CST 00'].iloc[linha])
            cst10 = formatar_sim_ou_nao(tabela['CST 10'].iloc[linha])
            cst20 = formatar_sim_ou_nao(tabela['CST 20'].iloc[linha])
            cst30 = formatar_sim_ou_nao(tabela['CST 30'].iloc[linha])
            cst40 = formatar_sim_ou_nao(tabela['CST 40'].iloc[linha])
            cst41 = formatar_sim_ou_nao(tabela['CST 41'].iloc[linha])            
            cst50 = formatar_sim_ou_nao(tabela['CST 50'].iloc[linha])
            cst51 = formatar_sim_ou_nao(tabela['CST 51'].iloc[linha])
            cst53 = formatar_sim_ou_nao(tabela['CST 53'].iloc[linha])
            cst60 = formatar_sim_ou_nao(tabela['CST 60'].iloc[linha])
            cst70 = formatar_sim_ou_nao(tabela['CST 70'].iloc[linha])
            cst90 = formatar_sim_ou_nao(tabela['CST 90'].iloc[linha])                                                                                
            
            sql_insert = gerar_comando_sql_insert(codigo_beneficio, descricao, tipo_beneficio, uf, cst00, cst10, cst20, cst30, cst40, cst41, cst50, cst51, cst53, cst60, cst70, cst90, data_inicio, data_fim)
            lista_sql.append(sql_insert)

    nome_arquivo_texto = alterar_extencao(arquivo_pdf, '.txt')
    salvar_texto(lista_sql, nome_arquivo_texto)


arquivo_cebenef_sc = "D:\\Documentacao\\Escrita Fiscal\\Manuais\\NFe_NFCe\\Beneficio Fiscal\\Santa Catarina - Tabela cBenef por CST v5.2.pdf"
importar_tabela_santa_catarina(arquivo_cebenef_sc)


    
    