# KMS Signature Verifier

Professional toolkit for offline KMS signature verification, audit logging, and cryptographic proof generation.

## 🎯 Features

✅ **Offline KMS Signature Verification**
- Support for RSA (PKCS1v15) and ECDSA signatures
- SHA-256 fingerprint computation
- DER/PEM key format support
- Structured logging

✅ **Key Management**
- Base64 → DER/PEM conversion
- SHA-256 fingerprint extraction
- Key validation and verification

✅ **GPG Message Signing**
- Detached signature generation
- Multi-backend support (python-gnupg + CLI)
- JSON report generation
- Cryptographic audit trails

✅ **GitHub Actions Integration**
- Automated verification workflow
- Artifact management
- Workflow summary reporting
- RBAC permissions

✅ **Production Ready**
- Comprehensive error handling
- Input validation
- Timeout protection
- Security best practices

## 📂 Repository Structure

```
kms-signature-verifier/
├── verify_kms_signature.py       # KMS signature verifier (offline)
├── convert_public_key.py          # Public key converter (base64 → DER/PEM)
├── sign_and_verify_msg.py         # GPG message signing & verification
├── sign_and_verify_msg.sh         # Bash wrapper
├── requirements.txt               # Python dependencies
├── .github/
│   └── workflows/
│       └── verify-and-upload.yml  # GitHub Actions workflow
├── tests/
│   ├── test_verify_kms_signature.py
│   ├── test_convert_public_key.py
│   ├── test_sign_and_verify_msg.py
│   └── fixtures/                  # Test data
├── examples/
│   ├── audit_log_example.json
│   └── usage_examples.md
├── docs/
│   ├── SECURITY.md
│   ├── DEPLOYMENT.md
│   ├── ARCHITECTURE.md
│   └── TROUBLESHOOTING.md
└── docker/
    ├── Dockerfile
    └── docker-compose.yml
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify KMS Signature (Offline)

```bash
python3 verify_kms_signature.py \
  --file audit_log.json \
  --sig audit_log.json.sig \
  --pub kms_public.der \
  --verbose
```

### 3. Convert Public Key from Base64

```bash
python3 convert_public_key.py \
  --in public_key_base64.txt \
  --out-der kms_public.der \
  --out-pem kms_public.pem
```

### 4. Create Signed Confirmation

```bash
python3 sign_and_verify_msg.py \
  --text "Confirm fingerprint: 3A:7F:..." \
  --workflow-run-id 12345 \
  --commit-hash abc123 \
  --workflow-repo myorg/myrepo \
  --workflow-ref refs/heads/main
```

## 📊 Output Example

### KMS Signature Verification

```
Public key SHA-256 fingerprint (SubjectPublicKeyInfo DER): 3A:7F:1C:9B:4E:2D:8A:5E:11:6F:2B:90:4C:AA:77:2D:9E:5B:3C:8F
VERIFIED OK (RSA PKCS1v15, SHA-256)
```

### JSON Report

```json
{
  "result": "VERIFIED_OK",
  "key_id": "0xABCDEF1234567890",
  "fingerprint": "3A7F1C9B4E2D8A5E116F2B904CAA772D9E5B3C8F",
  "gpg_timestamp": "2026-07-04T23:10:00Z",
  "iso_timestamp_utc": "2026-07-04T21:37:00+00:00",
  "workflow_run_id": "12345",
  "commit_hash": "9f2b7c3",
  "workflow_repo": "myorg/myrepo",
  "workflow_ref": "refs/heads/main"
}
```

## 🔒 Security Features

| Feature | Description |
|---------|-------------|
| **Offline Verification** | Run on isolated machine without internet |
| **Fingerprint Validation** | Compare fingerprints via independent channels |
| **Input Validation** | All inputs validated before processing |
| **Timeout Protection** | 30-second timeout on all commands |
| **Error Handling** | Comprehensive error logging and reporting |
| **RBAC** | GitHub Actions with minimal permissions |

## 📋 Exit Codes

| Code | Meaning |
|------|---------|
| 0 | ✅ Success (signature valid / operation completed) |
| 1 | ⚠️ IO error or usage error |
| 2 | ❌ Signature invalid |
| 3 | ⚠️ Unsupported key type or other error |

## 🐳 Docker Support

### Build Image

```bash
docker build -f docker/Dockerfile -t kms-verifier:latest .
```

### Run in Container

```bash
docker run --rm -v $(pwd):/work kms-verifier:latest \
  python3 verify_kms_signature.py \
  --file /work/audit_log.json \
  --sig /work/audit_log.json.sig \
  --pub /work/kms_public.der
```

## 🧪 Testing

### Run Unit Tests

```bash
pytest tests/ -v --cov=. --cov-report=html
```

### Run with Coverage

```bash
pytest tests/ --cov --cov-report=term-missing
```

## 📚 Documentation

- **[SECURITY.md](SECURITY.md)** — Security policy and best practices
- **[DEPLOYMENT.md](DEPLOYMENT.md)** — Production deployment guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — System design and components
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — Common issues and solutions

## 🔄 GitHub Actions Workflow

Trigger verification workflow:

```bash
gh workflow run verify-and-upload.yml \
  -f audit_log_path=audit_log.json \
  -f public_key_path=kms_public.der
```

Or use repository_dispatch:

```bash
gh api repos/OPKOP-TRIVIUM-sha365/kms-signature-verifier/dispatches \
  -f event_type=audit_ready
```

## 🤝 Contributing

Contributions welcome! See CONTRIBUTING.md for guidelines.

## ⚖️ License
License
This project is licensed under the KMS Signature Verifier License (KSVL) 1.0 — see LICENSE for details.


## 📧 Support

For issues and questions:
- GitHub Issues: [Report an issue](https://github.com/OPKOP-TRIVIUM-sha365/kms-signature-verifier/issues)
- Security: See SECURITY.md for responsible disclosure

---

**Made by:** Vildan KULJANOVIĆ (OPKOP-TRIVIUM-sha365)  
**Last Updated:** 2026-07-04  
**Status:** Production Ready ✅
