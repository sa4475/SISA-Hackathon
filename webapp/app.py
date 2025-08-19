import os
import sqlite3
from pathlib import Path
from typing import List, Tuple

from flask import Flask, request, render_template
from jinja2 import Environment, BaseLoader


APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "demo.db"


def ensure_database_seeded() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL
            )
            """
        )
        conn.commit()

        cur.execute("SELECT COUNT(1) FROM users")
        count = cur.fetchone()[0]
        if count == 0:
            demo_rows = [
                ("admin", "admin@example.com"),
                ("alice", "alice@corp.local"),
                ("bob", "bob@corp.local"),
                ("charlie", "charlie@corp.local"),
            ]
            cur.executemany("INSERT INTO users(username, email) VALUES(?, ?)", demo_rows)
            conn.commit()
    finally:
        conn.close()


def unsafe_sqli_search(query_text: str) -> List[Tuple[int, str, str]]:
    # Intentionally vulnerable: string concatenation enables SQLi for demo purposes.
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        sql = (
            "SELECT id, username, email FROM users "
            f"WHERE username LIKE '%{query_text}%' OR email LIKE '%{query_text}%'"
        )
        cur.execute(sql)
        return cur.fetchall()
    finally:
        conn.close()


def render_user_template(user_template: str) -> str:
    # Intentionally unsafe: renders attacker-controlled template (SSTI demo)
    env = Environment(loader=BaseLoader(), autoescape=False)
    tmpl = env.from_string(user_template)
    return tmpl.render()


def create_app() -> Flask:
    ensure_database_seeded()
    app = Flask(__name__, template_folder=str(APP_DIR / "templates"))

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/xss")
    def xss():
        payload = request.args.get("payload", "")
        return render_template("xss.html", payload=payload)

    @app.get("/ssti")
    def ssti():
        template_text = request.args.get("template", "Hello {{ 7*7 }}")
        try:
            rendered = render_user_template(template_text)
        except Exception as e:
            rendered = f"Error rendering template: {e}"
        return render_template("ssti.html", template_text=template_text, rendered=rendered)

    @app.get("/sqli")
    def sqli():
        q = request.args.get("q", "")
        results: List[Tuple[int, str, str]] = []
        error_msg = ""
        if q:
            try:
                results = unsafe_sqli_search(q)
            except Exception as e:
                error_msg = str(e)
        return render_template("sqli.html", q=q, results=results, error_msg=error_msg)

    return app


if __name__ == "__main__":
    port_str = os.getenv("PORT", "5000")
    try:
        port = int(port_str)
    except ValueError:
        port = 5000
    app = create_app()
    app.run(host="127.0.0.1", port=port, debug=False)




