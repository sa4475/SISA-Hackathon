import csv
from collections import Counter

# Lightweight recon without external deps: frequency + n-gram rarity

def load_urls_from_csv(path: str) -> list[str]:
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row['URL'] for row in reader if 'URL' in row and row['URL']]


def generate_ngrams(url: str, n_min: int = 1, n_max: int = 3) -> list[str]:
    tokens = [t for t in url.replace('?', '/').replace('&', '/').split('/') if t]
    ngrams: list[str] = []
    for n in range(n_min, n_max + 1):
        for i in range(len(tokens) - n + 1):
            ngrams.append('/'.join(tokens[i:i + n]))
    return ngrams or [url]


def score_url_rarity(url: str, ngram_counts: Counter) -> float:
    ngrams = generate_ngrams(url)
    # Lower average frequency => rarer => higher anomaly score (invert)
    freqs = [ngram_counts[ng] for ng in ngrams]
    avg_freq = sum(freqs) / max(len(freqs), 1)
    return 1.0 / (avg_freq + 1.0)


def main() -> None:
    urls = load_urls_from_csv('access_logs.csv')
    if not urls:
        print("No URLs loaded. Ensure access_logs.csv exists with a 'URL' column.")
        return

    # Build global n-gram frequency map
    ngram_counts: Counter = Counter()
    for url in urls:
        ngram_counts.update(generate_ngrams(url))

    # Compute rarity score for each URL
    url_scores = [(url, score_url_rarity(url, ngram_counts)) for url in urls]

    # Show top-K rare/odd endpoints (unique order preserved by score)
    unique_seen = set()
    unique_scored = []
    for url, score in sorted(url_scores, key=lambda x: x[1], reverse=True):
        if url not in unique_seen:
            unique_seen.add(url)
            unique_scored.append((url, score))
        if len(unique_scored) >= 8:
            break

    print("Potential hidden/odd endpoints:")
    for url, score in unique_scored:
        print(f"- {url} (rarity_score={score:.3f})")


if __name__ == '__main__':
    main()
