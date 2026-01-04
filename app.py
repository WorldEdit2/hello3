from flask import Flask, render_template_string, request
import sqlite3
import os

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
    <title>Buluttan Selam!</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
        h1 { color: #333; }
        form { margin: 20px auto; }
        input { padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
        button:hover { background: #45a049; }
        ul { list-style: none; padding: 0; }
        li { background: white; margin: 5px auto; width: 300px; padding: 10px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <h1>Buluttan Selam! (SQLite) ☁️</h1>
    
    <form method="POST">
        <input type="text" name="mesaj" placeholder="Bir şeyler yaz..." required>
        <button type="submit">Gönder</button>
    </form>

    <h3>Kaydedilen Mesajlar:</h3>
    <ul>
        {% for item in items %}
            <li>{{ item }}</li>
        {% else %}
            <li>Henüz mesaj yok.</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

def get_db_connection():
    # SQLite veritabanı dosyası oluşturur (database.db)
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()

    if request.method == 'POST':
        yeni_mesaj = request.form['mesaj']
        conn.execute('INSERT INTO messages (content) VALUES (?)', (yeni_mesaj,))
        conn.commit()

    mesajlar = conn.execute('SELECT content FROM messages ORDER BY id DESC').fetchall()
    conn.close()

    # Veriyi listeye çevir
    temiz_liste = [mesaj['content'] for mesaj in mesajlar]
    
    return render_template_string(HTML, items=temiz_liste)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
