from database import c, conn

def atualizar_pontuacao(player_id, pontos):
    c.execute("SELECT score FROM players WHERE id=?", (player_id,))
    res = c.fetchone()
    if res:
        c.execute("UPDATE players SET score = score + ? WHERE id=?", (pontos, player_id))
    else:
        c.execute("INSERT INTO players (id, name, score) VALUES (?, ?, ?)", (player_id, "Jogador", pontos))
    conn.commit()

def ranking():
    c.execute("SELECT name, score FROM players ORDER BY score DESC LIMIT 10")
    return c.fetchall()
