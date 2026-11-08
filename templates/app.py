
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Ket noi co so du lieu
def get_db():
    conn = sqlite3.connect("news.db")
    conn.row_factory = sqlite3.Row
    return conn

# Tao bang tin tuc
def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Trang chu
@app.route("/")
def index():
    conn = get_db()

    news_list = conn.execute(
        "SELECT * FROM news ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("index.html", news_list=news_list)

# Trang chi tiet
@app.route("/detail/<int:id>")
def detail(id):
    conn = get_db()

    article = conn.execute(
        "SELECT * FROM news WHERE id = ?", (id,)
    ).fetchone()

    conn.close()

    return render_template("detail.html", article=article)

# Them tin tuc
@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    content = request.form["content"]

    conn = get_db()

    conn.execute(
        "INSERT INTO news (title, content) VALUES (?, ?)",
        (title, content)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))

# Xoa tin tuc
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db()

    conn.execute(
        "DELETE FROM news WHERE id = ?", (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
