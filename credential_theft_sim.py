import os


def mask_secret(secret: str, show_start: int = 2, show_end: int = 2) -> str:
    if not secret:
        return ""
    if len(secret) <= show_start + show_end:
        return "*" * len(secret)
    return f"{secret[:show_start]}{'*' * (len(secret) - show_start - show_end)}{secret[-show_end:]}"


def main() -> None:
    print("[Credential Theft Simulation]")
    key = os.getenv("OPENAI_API_KEY", "")
    if key:
        print("- OPENAI_API_KEY detected in environment (masked):", mask_secret(key))
        print(f"- Key length: {len(key)} characters")
    else:
        print("- No OPENAI_API_KEY found in environment.")

    print("\nHardening tips:")
    print("- Store secrets in environment variables or a secure vault, not in code.")
    print("- Never print full secrets; mask when logging.")
    print("- Scope keys minimally and rotate regularly.")
    print("- In CI/automation, use per-job tokens that expire.")


if __name__ == "__main__":
    main()


