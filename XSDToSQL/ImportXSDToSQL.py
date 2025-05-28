import xml.etree.ElementTree as ET
import uuid
import sys
import os

def parse_xsd_and_generate_inserts(xsd_path, output_sql_path, table_name, last_id = 0):
    try:
        # Carrega o arquivo XSD
        tree = ET.parse(xsd_path)
        root = tree.getroot()
        
        # Define o namespace padrão (modifique conforme o XSD)
        namespaces = {'xs': 'http://www.w3.org/2001/XMLSchema'}
        
        sql_inserts = []
        id_value = last_id
        
        # Itera sobre os elementos do XSD
        for element in root.findall(".//xs:element", namespaces):
            element_name = element.get('name', '')
            #element_type = element.get('type', 'string')  # Assume "string" se o tipo não for especificado
            
            # Busca por documentação associada ao elemento
            documentation = 'NULL'
            annotation = element.find("xs:annotation/xs:documentation", namespaces)
            if annotation is not None and annotation.text:
                documentation = annotation.text.strip().replace("'", "''")  # Escapa apóstrofos
            
            # Cria os valores para os campos
            id_value += 1  #'custom_id_func' or str(uuid.uuid4().int)[:8]
            chave_value = element_name[:50]
            valor_value = documentation[:200] if documentation != 'NULL' else 'NULL'
            
            # Gera a instrução SQL INSERT
            layout_value =  os.path.basename(xsd_path);
            tipo_value = 'Tag'

            sql = f"INSERT INTO {table_name} (ID, Layout, Tipo, Chave, Valor) VALUES ({id_value}, '{layout_value}', '{tipo_value}', '{chave_value}', '{valor_value}');"
            sql_inserts.append(sql)
        
        # Escreve os inserts no arquivo de saída
        with open(output_sql_path, 'w') as sql_file:
            sql_file.write('\n'.join(sql_inserts))
        
        print(f"Inserts gerados com sucesso no arquivo: {output_sql_path}")
    
    except Exception as e:      
        print(f"Erro ao processar o arquivo XSD: {e}")

if __name__ == "__main__":
    # Verifica se os argumentos foram fornecidos
    if len(sys.argv) < 3:
        print("Uso: python ImportXSDToSQL.py <caminho_arquivo_xsd> <table_name> <ultimo_id_opcional>")
        sys.exit(1)
    
    # Lê os caminhos dos arquivos da linha de comando
    xsd_file_path = sys.argv[1]
    sql_output_path = os.path.splitext(xsd_file_path)[0]+'.sql'
    
    table_name = sys.argv[2]

    if len(sys.argv) == 4:
        last_id = sys.argv[3]
    else:    
        last_id = 0

    # Executa a função
    parse_xsd_and_generate_inserts(xsd_file_path, sql_output_path, table_name, int(last_id))