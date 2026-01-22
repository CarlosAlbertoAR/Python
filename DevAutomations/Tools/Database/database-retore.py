import os
import zipfile
import py7zr
import pyodbc
import logging

# Melhorias
# 1 - Input para job_name
# 2 - Constante com diretório de destino: E:\Base de dados\SQL Server\ + [job_name]
# 3 - Verificar também arquivos rar ao descompactar
# 4 - Identificar o tipo de arquivo sql server, sybase ou postgres (arquivos sem extensão)
# 5 - Comandos SQL pos extração
#

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_file(file_path):
    """
    Descompacta arquivos .zip ou .7z e retorna o caminho do arquivo .bak encontrado.
    """
    extract_path = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    
    if filename.lower().endswith('.zip'):
        logging.info(f"Extraindo ZIP: {filename}")
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    
    elif filename.lower().endswith('.7z'):
        logging.info(f"Extraindo 7z: {filename}")
        with py7zr.SevenZipFile(file_path, mode='r') as z:
            z.extractall(path=extract_path)
            
    # Se já for um arquivo .bak, apenas retorna o caminho
    if filename.lower().endswith('.bak'):
        return file_path

    # Procura pelo arquivo .bak na pasta após a extração
    for root, dirs, files in os.walk(extract_path):
        for file in files:
            if file.lower().endswith('.bak'):
                return os.path.join(root, file)
    
    return None

def restore_sql_server_backup(bak_path, db_name, server='localhost', user=None, password=None):
    """
    Restaura o arquivo .bak para o SQL Server.
    """
    try:
        # Configuração da string de conexão (Autenticação Windows ou SQL)
        if user and password:
            conn_str = f'DRIVER={{SQL Server}};SERVER={server};UID={user};PWD={password};DATABASE=master'
        else:
            conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE=master;Trusted_Connection=yes'
        
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()

        logging.info(f"Obtendo informações lógicas do backup: {bak_path}")
        
        # 1. Identificar nomes lógicos dos arquivos dentro do backup (Data e Log)
        cursor.execute(f"RESTORE FILELISTONLY FROM DISK = '{bak_path}'")
        files = cursor.fetchall()
        
        # Geralmente o primeiro é DATA (mdf) e o segundo é LOG (ldf)
        logical_data = files[0].LogicalName
        logical_log = files[1].LogicalName

        # 2. Comando de restauração com REPLACE e MOVE (para garantir que vá para o diretório padrão do servidor)
        # Nota: Em um script de produção, você pode querer customizar o caminho de destino dos arquivos mdf/ldf
        restore_query = f"""
        RESTORE DATABASE [{db_name}]
        FROM DISK = '{bak_path}'
        WITH REPLACE,
        MOVE '{logical_data}' TO '{os.path.join(os.path.dirname(bak_path), db_name + ".mdf")}',
        MOVE '{logical_log}' TO '{os.path.join(os.path.dirname(bak_path), db_name + "_log.ldf")}'
        """
        
        logging.info(f"Iniciando restauração da base [{db_name}]...")
        cursor.execute(restore_query)
        
        while cursor.nextset(): # Aguarda a conclusão de todos os processos do SQL
            pass
            
        logging.info("Restauração concluída com sucesso!")
        
    except Exception as e:
        logging.error(f"Erro ao restaurar banco de dados: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def main():
    # Solicitação de dados ao usuário
    file_input = input("Digite o caminho completo do arquivo (.zip, .7z ou .bak): ").strip('"')
    
    if not os.path.exists(file_input):
        print("Arquivo não encontrado!")
        return

    bak_file = extract_file(file_input)
    
    if bak_file:
        print(f"Arquivo de backup identificado: {bak_file}")
        db_target = input("Digite o nome da base de dados para a restauração: ")
        
        # Parâmetros de conexão (ajuste conforme seu ambiente)
        sql_server = input("Servidor SQL (Padrão: localhost): ") or "localhost"
        
        restore_sql_server_backup(bak_file, db_target, server=sql_server)
    else:
        print("Não foi possível localizar um arquivo .bak no caminho fornecido.")

if __name__ == "__main__":
    main()