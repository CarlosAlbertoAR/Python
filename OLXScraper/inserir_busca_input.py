import sqlite3

def inserir_busca():
    conn = sqlite3.connect("olx_bot.db")
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS buscas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ativo INTEGER,
        categoria TEXT,
        descricao TEXT,
        valor_minimo REAL,
        valor_maximo REAL,
        localizacao TEXT,
        ordenacao TEXT,
        link TEXT,
        destinatario_telegram TEXT,
        data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP,
        data_ultima_busca TEXT,
        ultimo_id_encontrado TEXT
    )
    ''')

    print("== Inserir nova busca ==")
    ativo = int(input("Ativa (1=Sim, 0=Não): "))
    categoria = input("Categoria (ex: carros, imoveis): ").strip()
    descricao = input("Descrição da busca: ").strip()
    valor_minimo = input("Valor mínimo (ou deixe em branco): ").strip()
    valor_maximo = input("Valor máximo (ou deixe em branco): ").strip()
    localizacao = input("Filtro por localização (ex: Goiânia): ").strip()
    ordenacao = input("Ordenação (relevancia, data): ").strip()
    link = input("Link completo da OLX com os filtros aplicados: ").strip()
    destinatario = input("ID do destinatário no Telegram: ").strip()

    valor_minimo = float(valor_minimo) if valor_minimo else None
    valor_maximo = float(valor_maximo) if valor_maximo else None

    c.execute('''INSERT INTO buscas (
        ativo, categoria, descricao, valor_minimo, valor_maximo,
        localizacao, ordenacao, link, destinatario_telegram
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        ativo, categoria, descricao, valor_minimo, valor_maximo,
        localizacao, ordenacao, link, destinatario
    ))

    conn.commit()
    conn.close()
    print("Busca cadastrada com sucesso!")

if __name__ == "__main__":
    inserir_busca()
