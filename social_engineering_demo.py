from __future__ import annotations


def main() -> None:
    print("[Social Engineering via AI Demo]")
    print("Example phishing-style outputs (for awareness training):\n")
    print("- Subject: Urgent: Account Verification Required")
    print("  Body: Your account was flagged. Verify within 24h at https://corp.example.com-verify ...")
    print("\nMitigations:")
    print("- Banner labeling external emails, DMARC/SPF/DKIM, user education.")
    print("- Add friction for sensitive actions (MFA, step-up auth).")


if __name__ == "__main__":
    main()


