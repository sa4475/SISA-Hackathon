from __future__ import annotations

import concurrent.futures
import time
from http.client import HTTPConnection


def ping(host: str, port: int, path: str = "/", timeout: float = 2.0) -> int:
    try:
        conn = HTTPConnection(host, port, timeout=timeout)
        conn.request("GET", path)
        resp = conn.getresponse()
        code = resp.status
        conn.close()
        return code
    except Exception:
        return 0


def main() -> None:
    host, port = "127.0.0.1", 5000
    total = 300
    print(f"[DoS Attack Simulation] Flooding http://{host}:{port} with {total} requests...")
    start = time.time()
    successes = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
        futures = [ex.submit(ping, host, port, "/") for _ in range(total)]
        for fut in concurrent.futures.as_completed(futures):
            if fut.result() == 200:
                successes += 1
    elapsed = time.time() - start
    print(f"Completed in {elapsed:.2f}s with {successes}/{total} HTTP 200 responses")
    print("Observation: Local server may start failing if overwhelmed; implement rate limits.")


if __name__ == "__main__":
    main()


