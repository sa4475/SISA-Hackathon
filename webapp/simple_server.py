import html
import sqlite3
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler


DB_PATH = "webapp_demo.sqlite3"


def ensure_db():
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
        (count,) = cur.fetchone()
        if count == 0:
            cur.executemany(
                "INSERT INTO users(username, email) VALUES(?, ?)",
                [
                    ("admin", "admin@example.com"),
                    ("alice", "alice@corp.local"),
                    ("bob", "bob@corp.local"),
                ],
            )
            conn.commit()
    finally:
        conn.close()


INDEX_HTML = b"""<!doctype html>
<html>
  <head>
    <meta charset=\"utf-8\" />
    <title>Basic Vuln Demos</title>
  </head>
  <body>
    <h1>Basic Vulnerable Website (no deps)</h1>
    <ul>
      <li><a href=\"/xss?payload=%3Csvg%20onload%3Dalert(1)%3E\">XSS demo</a></li>
      <li><a href=\"/ssti?expr=7*7\">SSTI-like eval demo</a></li>
      <li><a href=\"/sqli?q=%27%20OR%20%271%27%3D%271%27%20--\">SQLi demo</a></li>
    </ul>
  </body>
  </html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path)
        route = parsed.path
        params = parse_qs(parsed.query)

        if route == "/":
            self._ok_html(INDEX_HTML)
            return

        if route == "/xss":
            payload = params.get("payload", [""])[0]
            # Intentionally vulnerable: reflect unescaped
            body = f"""
            <!doctype html><html><body>
            <h1>XSS</h1>
            <div>Reflected payload below (dangerously unescaped):</div>
            <div style='padding:8px;border:1px solid #ccc'>{payload}</div>
            <p><a href='/'>Back</a></p>
            </body></html>
            """.encode("utf-8")
            self._ok_html(body)
            return

        if route == "/ssti":
            expr = params.get("expr", ["7*7"])[0]
            # Intentionally unsafe: eval user-controlled expression
            try:
                result = str(eval(expr, {"__builtins__": {}}, {}))  # nosec - demo only
            except Exception as e:  # noqa: BLE001
                result = f"Error: {e}"
            body = f"""
            <!doctype html><html><body>
            <h1>SSTI-like</h1>
            <div>Expression: <code>{html.escape(expr)}</code></div>
            <div>Result: <strong>{html.escape(result)}</strong></div>
            <p><a href='/'>Back</a></p>
            </body></html>
            """.encode("utf-8")
            self._ok_html(body)
            return

        if route == "/sqli":
            q = params.get("q", [""])[0]
            rows = []
            error = None
            if q:
                try:
                    conn = sqlite3.connect(DB_PATH)
                    cur = conn.cursor()
                    # Intentionally vulnerable: concatenation enabling SQLi
                    sql = (
                        "SELECT id, username, email FROM users "
                        f"WHERE username LIKE '%{q}%' OR email LIKE '%{q}%'"
                    )
                    cur.execute(sql)
                    rows = cur.fetchall()
                except Exception as e:  # noqa: BLE001
                    error = str(e)
                finally:
                    try:
                        conn.close()
                    except Exception:
                        pass
            table = "".join(
                f"<tr><td>{r[0]}</td><td>{html.escape(r[1])}</td><td>{html.escape(r[2])}</td></tr>"
                for r in rows
            )
            body = f"""
            <!doctype html><html><body>
            <h1>SQL Injection</h1>
            <form method='get' action='/sqli'>
              <label>Search: <input name='q' value='{html.escape(q)}'></label>
              <button type='submit'>Go</button>
            </form>
            {f"<p style='color:red'>Error: {html.escape(error)}</p>" if error else ''}
            <table border='1' cellpadding='6'><tr><th>ID</th><th>Username</th><th>Email</th></tr>{table}</table>
            <p><a href='/'>Back</a></p>
            </body></html>
            """.encode("utf-8")
            self._ok_html(body)
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Not found")

    def _ok_html(self, content: bytes) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    ensure_db()
    httpd = HTTPServer((host, port), Handler)
    print(f"Serving on http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()


