import sqlite3

conn = sqlite3.connect('forca.db', check_same_thread=False)
c = conn.cursor()

# Tabelas
c.execute('''
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY, 
    name TEXT, 
    score INTEGER DEFAULT 0
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS words (
    word TEXT PRIMARY KEY, 
    hint TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS tournament (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    points INTEGER
)
''')

# Inserir algumas palavras iniciais
palavras = [
    ("python", "Linguagem de programação popular"),
    ("telegram", "Aplicativo de mensagens"),
    ("railway", "Plataforma para deploy de bots")
]
c.executemany("INSERT OR IGNORE INTO words (word, hint) VALUES (?,?)", palavras)
conn.commit()
