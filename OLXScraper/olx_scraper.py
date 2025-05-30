# pip install requests beautifulsoup4
import sqlite3
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

# Constantes
INTERVALO_MINUTOS = 10
TOKEN_TELEGRAM = '7660507190:AAEiO1u1WGPyO_L9sIcKGKZb5HGzAEsav-4'

# Inicializa banco de dados
def criar_db():
    conn = sqlite3.connect("olx_bot.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS buscas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ativo INTEGER NOT NULL,
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
            ultimo_id_enviado TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS anuncios_enviados (
            id TEXT PRIMARY KEY,
            id_busca INTEGER,
            preco_anterior REAL
        )
    ''')
    conn.commit()
    conn.close()

# Realiza a busca no site da OLX
def buscar_anuncios(link, ultimo_id=None):
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    anuncios = []

    for item in soup.select('[data-lurker-detail="list_id"]')[:12]:
        try:
            id_anuncio = item['data-lurker-list-id']
            if ultimo_id and id_anuncio <= ultimo_id:
                continue
            titulo = item.select_one("h2").text.strip()
            preco_raw = item.select_one("p").text.strip()
            preco = float(preco_raw.replace('R$', '').replace('.', '').replace(',', '.'))
            link_item = item.find("a")["href"]
            img = item.select_one('img')
            imagem = img['src'] if img and 'src' in img.attrs else ''
            anuncios.append({
                "id": id_anuncio,
                "titulo": titulo,
                "preco": preco,
                "preco_str": preco_raw,
                "link": f"https://www.olx.com.br{link_item}",
                "imagem": imagem
            })
        except:
            continue
    return anuncios

# Envia os anúncios via Telegram
def enviar_telegram(token, chat_id, anuncios, enviados_anteriormente):
    for a in anuncios:
        preco_antigo = enviados_anteriormente.get(a['id'])
        preco_foi_reduzido = preco_antigo and a['preco'] < preco_antigo
        if a['id'] not in enviados_anteriormente or preco_foi_reduzido:
            mensagem = f"📢 *{a['titulo']}*\n💰 {a['preco_str']}"
            if preco_foi_reduzido:
                mensagem += f"\n📉 Preço anterior: R$ {preco_antigo:.2f}"
            mensagem += f"\n🔗 [Ver anúncio]({a['link']})"
            if a['imagem']:
                requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data={
                    "chat_id": chat_id,
                    "caption": mensagem,
                    "parse_mode": "Markdown",
                    "photo": a['imagem']
                })
            else:
                requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={
                    "chat_id": chat_id,
                    "text": mensagem,
                    "parse_mode": "Markdown"
                })

# Executa o loop principal
def executar_loop():
    while True:
        conn = sqlite3.connect("olx_bot.db")
        c = conn.cursor()

        c.execute("SELECT * FROM buscas WHERE ativo = 1")
        buscas = c.fetchall()

        if len(buscas) == 0:
            print('Nenhuma busca cadastrada.')

        for busca in buscas:
            (id_busca, _, _, _, val_min, val_max, localizacao, _, link,
             chat_id, _, _, ultimo_id) = busca

            anuncios = buscar_anuncios(link, ultimo_id)

            enviados_anteriormente = {
                row[0]: row[1] for row in c.execute(
                    "SELECT id, preco_anterior FROM anuncios_enviados WHERE id_busca = ?", (id_busca,)
                )
            }

            novos_anuncios = [a for a in anuncios if
                              (val_min is None or a['preco'] >= val_min) and
                              (val_max is None or a['preco'] <= val_max) and
                              (localizacao.lower() in a['titulo'].lower())]

            if novos_anuncios:
                enviar_telegram(TOKEN_TELEGRAM, chat_id, novos_anuncios, enviados_anteriormente)
                novo_ultimo_id = novos_anuncios[0]['id']
                c.execute("UPDATE buscas SET ultimo_id_enviado = ?, data_ultima_busca = ? WHERE id = ?",
                          (novo_ultimo_id, datetime.now(), id_busca))
                for a in novos_anuncios:
                    c.execute('''INSERT OR REPLACE INTO anuncios_enviados (id, id_busca, preco_anterior)
                                 VALUES (?, ?, ?)''', (a['id'], id_busca, a['preco']))
        conn.commit()
        conn.close()
        print(f'Nova busca sera efetuada em {INTERVALO_MINUTOS} minutos.')
        time.sleep(INTERVALO_MINUTOS * 60)


if __name__ == "__main__":
    criar_db()
    executar_loop()
