"""
executar_job.py

Script de linha de comando que usa as classes BackupRestoreJob e
DatabaseServer (backup_restore_job.py) para rodar um job de restauração
de backup de forma interativa.

Para uso programático (ex: dentro de uma rotina agendada, sem prompts),
importe as classes diretamente:

    from backup_restore_job import BackupRestoreJob, DatabaseServer

    server = DatabaseServer(server="localhost", user="sa", password="Senha123!")
    job = BackupRestoreJob(
        file_input=r"\\\\fileserver\\backups\\base.zip",
        destination_folder=r"C:\\restores",
        db_target="MinhaBase",
        server=server,
        delete_extracted_backup=True,
        post_restore_scripts=[r"scripts\\pos_restore.sql"],
    )
    ok = job.run()
    print(job.to_dict())
"""

from backup_restore import BackupRestore, DatabaseServer


def main():
    print("=== Job de restauração de backup ===\n")

    file_input = input(
        "Caminho completo do arquivo de backup (local ou de rede; "
        ".zip, .7z, .rar, .bak, .sql, etc.): "
    ).strip('"')

    destination_folder = input("Pasta base de destino para extração: ").strip('"')
    db_target = input("Nome da base de dados de destino: ").strip()

    server_name = input("Servidor (Padrão: localhost): ").strip() or "localhost"
    user = input("Usuário (deixe em branco para autenticação integrada, quando suportado): ").strip() or None
    password = input("Senha: ") if user else None
    driver = input("Driver ODBC (deixe em branco para usar o padrão da classe): ").strip() or None

    trusted_input = input("Usar autenticação integrada/confiável (s/N)? ").strip().lower()
    trusted_connection = trusted_input == 's' or user is None

    delete_extracted_input = input(
        "Excluir o backup extraído após a restauração (não afeta o arquivo de origem)? (s/N): "
    ).strip().lower()
    delete_extracted_backup = delete_extracted_input == 's'

    server = DatabaseServer(
        server=server_name,
        database=db_target,
        user=user,
        password=password,
        driver=driver,
        trusted_connection=trusted_connection,
    )

    try:
        job = BackupRestoreJob(
            file_input=file_input,
            destination_folder=destination_folder,
            db_target=db_target,
            server=server,
            delete_extracted_backup=delete_extracted_backup,
            # Scripts SQL a rodar após uma restauração bem-sucedida.
            # Aceita caminho de arquivo .sql OU texto SQL direto na lista.
            post_restore_scripts=[],
        )
    except (FileNotFoundError, ValueError, TypeError) as exc:
        print(f"Erro ao criar o job: {exc}")
        return

    print(f"\nJob criado: {job}")
    print(f"Pasta de extração: {job.extraction_path}\n")

    ok = job.run()

    print("\n--- Log do job ---")
    for entry in job.log_entries:
        print(entry)

    print("\n--- Resumo ---")
    for key, value in job.to_dict().items():
        print(f"{key}: {value}")

    print("\nResultado final:", "SUCESSO" if ok else "FALHA")


if __name__ == "__main__":
    main()
