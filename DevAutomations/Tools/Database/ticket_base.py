"""
executar_ticket.py

Script de linha de comando que usa as classes BackupRestoreticket e
DatabaseServer (backup_restore.py) para rodar um ticket de restauração
de backup de forma interativa.

Para uso programático (ex: dentro de uma rotina agendada, sem prompts),
importe as classes diretamente:

    from backup_restore import BackupRestore, DatabaseServer

    server = DatabaseServer(server="localhost", user="sa", password="Senha123!")
    ticket = BackupRestore(
        file_input=r"\\\\fileserver\\backups\\base.zip",
        destination_folder=r"C:\\restores",
        db_target="MinhaBase",
        server=server,
        delete_extracted_backup=True,
        post_restore_scripts=[r"scripts\\pos_restore.sql"],
    )
    ok = ticket.run()
    print(ticket.to_dict())
"""


import sys
import os

#sys.path.append(os.path.abspath("./Database"))
#from Database.backup_restore import BackupRestore, ConnectionSettings

from backup_restore import BackupRestore, ConnectionSettings

def main():
    print("=== Restauração de backup ===\n")

    ticket_id = "35656"
    file_input = r"E:\Base de dados\SQL Server\35656\Data7_FCLOCKS.db"
    destination_folder = rf"E:\\Base de dados\SQL Server\{ticket_id}"

    server_name = "localhost"
    user = "sa"
    password = "se7e@123"
    driver = None
    database_name = "35656"
    trusted_input = False
    trusted_connection = trusted_input == "s" or user is None
    delete_extracted_backup = True # Excluir o backup extraído após a restauração (não afeta o arquivo de origem)

    post_restore_scripts = list() # .sql file or direct sql
    post_restore_scripts.append(reset_admin_password())
    post_restore_scripts.append(clear_entrada_sistema())

    connection = ConnectionSettings(
        server=server_name,
        database=database_name,
        user=user,
        password=password,
        driver=driver,
        trusted_connection=trusted_connection,
    )

    try:
        restore = BackupRestore(
            file_input=file_input,
            destination_folder=destination_folder,
            database_name=database_name,
            connection_settings=connection,
            ticket_id=ticket_id,
            delete_extracted_backup=delete_extracted_backup,
            post_restore_scripts=post_restore_scripts,
        )
    except (FileNotFoundError, ValueError, TypeError) as exc:
        print(f"Erro ao criar o restore: {exc}")
        return

    print(f"\nticket criado: {restore}")
    print(f"Pasta de extração: {restore.destination_folder}\n")

    ok = restore.run()

    print("\n--- Log do restore ---")
    for entry in restore.log_entries:
        print(entry)

    print("\n--- Resumo ---")
    for key, value in restore.to_dict().items():
        print(f"{key}: {value}")

    print("\nResultado final:", "SUCESSO" if ok else "FALHA")

def reset_admin_password():
    return "UPDATE Usuario SET Senha = '9055E34EFF' WHERE NomeLegivel = 'Administrador';"

def clear_entrada_sistema():
    return "DELETE FROM EntradaSistema"



if __name__ == "__main__":
    main()
