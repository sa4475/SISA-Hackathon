from webapp.app import create_app


def main() -> None:
    app = create_app()
    client = app.test_client()

    def check(path: str) -> None:
        resp = client.get(path)
        print(f"GET {path} -> {resp.status_code}, bytes={len(resp.data)}")

    check("/")
    check("/xss?payload=%3Csvg%20onload%3Dalert(1)%3E")
    check("/ssti?template=%7B%7B7*7%7D%7D")
    check("/sqli?q=%27%20OR%20%271%27%3D%271%27%20--")


if __name__ == "__main__":
    main()


