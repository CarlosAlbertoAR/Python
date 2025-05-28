import sqlite3
import tkinter as tk
from tkinter import messagebox

def salvar_busca():
    try:
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

        ativo = int(entry_ativo.get())
        categoria = entry_categoria.get().strip()
        descricao = entry_descricao.get().strip()
        valor_minimo = entry_valor_minimo.get().strip()
        valor_maximo = entry_valor_maximo.get().strip()
        localizacao = entry_localizacao.get().strip()
        ordenacao = entry_ordenacao.get().strip()
        link = entry_link.get().strip()
        destinatario = entry_destinatario.get().strip()

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
        messagebox.showinfo("Sucesso", "Busca cadastrada com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

# Interface gráfica
root = tk.Tk()
root.title("Cadastro de Busca - OLX Bot")

tk.Label(root, text="Ativo (1=Sim, 0=Não):").grid(row=0, column=0)
entry_ativo = tk.Entry(root)
entry_ativo.grid(row=0, column=1)

tk.Label(root, text="Categoria:").grid(row=1, column=0)
entry_categoria = tk.Entry(root)
entry_categoria.grid(row=1, column=1)

tk.Label(root, text="Descrição:").grid(row=2, column=0)
entry_descricao = tk.Entry(root)
entry_descricao.grid(row=2, column=1)

tk.Label(root, text="Valor Mínimo:").grid(row=3, column=0)
entry_valor_minimo = tk.Entry(root)
entry_valor_minimo.grid(row=3, column=1)

tk.Label(root, text="Valor Máximo:").grid(row=4, column=0)
entry_valor_maximo = tk.Entry(root)
entry_valor_maximo.grid(row=4, column=1)

tk.Label(root, text="Localização:").grid(row=5, column=0)
entry_localizacao = tk.Entry(root)
entry_localizacao.grid(row=5, column=1)

tk.Label(root, text="Ordenação:").grid(row=6, column=0)
entry_ordenacao = tk.Entry(root)
entry_ordenacao.grid(row=6, column=1)

tk.Label(root, text="Link OLX:").grid(row=7, column=0)
entry_link = tk.Entry(root, width=40)
entry_link.grid(row=7, column=1)

tk.Label(root, text="ID Telegram:").grid(row=8, column=0)
entry_destinatario = tk.Entry(root)
entry_destinatario.grid(row=8, column=1)

tk.Button(root, text="Salvar Busca", command=salvar_busca).grid(row=9, column=0, columnspan=2, pady=10)

root.mainloop()
