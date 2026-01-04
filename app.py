from flask import Flask, render_template_string, request
import os
import psycopg2

app = Flask(__name__)

# Veritabanı URL'sini ortam değişkeninden alıyoruz
DATABASE_URL = os.getenv("DATABASE_URL")

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
    <h1>Buluttan Selam! ☁️</h1>
    
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
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    """Veritabanı tablosunu oluşturur (eğer yoksa)"""
    if DATABASE_URL:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, content TEXT);')
        conn.commit()
        cur.close()
        conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Eğer DATABASE_URL ayarlı değilse hata vermemesi için basit kontrol
    if not DATABASE_URL:
        return "Hata: DATABASE_URL ortam değişkeni bulunamadı. Lütfen veritabanı bağlantısını ekleyin."

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        yeni_mesaj = request.form['mesaj']
        cur.execute('INSERT INTO messages (content) VALUES (%s)', (yeni_mesaj,))
        conn.commit()

    # Mesajları çek
    cur.execute('SELECT content FROM messages ORDER BY id DESC')
    mesajlar = cur.fetchall()
    
    cur.close()
    conn.close()

    # Veritabanından gelen veriyi liste (array) formatına çevirip HTML'e gönderiyoruz
    temiz_liste = [mesaj[0] for mesaj in mesajlar]
    
    return render_template_string(HTML, items=temiz_liste)

if __name__ == '__main__':
    # Uygulama başlarken tabloyu oluşturmayı dene
    try:
        init_db()
    except Exception as e:
        print(f"Veritabanı başlatma hatası: {e}")
        
    app.run(debug=True, host='0.0.0.0', port=5000)
