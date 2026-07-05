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

*** Begin Patch
*** Add File: LICENSE
+KMS Signature Verifier License (KSVL) 1.0
+SPDX-License-Identifier: KSVL-1.0
+
+Copyright (c) 2026 Vildan Kuljanović / OPKOP-TRIVIUM-sha365
+All rights reserved.
+
+Preamble
+This license governs use, reproduction, modification and distribution of the software
+and all accompanying materials in this repository (the "Software"). The intent is to
+permit broad use while preserving attribution, enabling auditability, and limiting
+liability for the author(s).
+
+Definitions
+"Software" means the source code, binaries, documentation, tests, examples, and other
+files included in this repository.
+"You" means any person or entity exercising rights under this License.
+
+Grant of Rights
+1. Permission is hereby granted, free of charge, to any person obtaining a copy of the
+   Software and associated documentation files, to use, copy, modify, merge, publish,
+   distribute, sublicense, and/or sell copies of the Software, subject to the
+   conditions set forth below.
+
+Conditions
+2. **Attribution**: Redistributions of source code must retain the above copyright
+   notice, this list of conditions and the following disclaimer in the top-level
+   LICENSE file and in any files that are modified.
+3. **NOTICE**: Redistributions in binary or compiled form must reproduce the above
+   copyright notice, this list of conditions and the following disclaimer in the
+   documentation and/or other materials provided with the distribution.
+4. **Changes**: If you modify the Software, you must include a clear notice in the
+   modified files and in the top-level documentation stating the nature of the
+   modifications and the date of modification.
+5. **No Endorsement**: You may not use the name of the copyright holder, contributors,
+   or project trademarks to endorse or promote products derived from the Software
+   without prior written permission.
+
+Patent Grant and Termination
+6. **Patent License**: Subject to the terms and conditions of this License, the
+   copyright holder and contributors hereby grant to You a perpetual, worldwide,
+   non-exclusive, no-charge, royalty-free, irrevocable (except as stated below)
+   patent license to make, have made, use, offer to sell, sell, import, and otherwise
+   transfer the Software.
+7. **Termination for Patent Litigation**: If You initiate patent litigation (including
+   a cross-claim or counterclaim) alleging that the Software infringes a patent,
+   then any patent licenses granted to You under this License for the Software shall
+   terminate as of the date such litigation is filed.
+
+Limitations and Disclaimer
+8. **No Warranty**: THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
+   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
+   FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. THE ENTIRE RISK ARISING OUT
+   OF USE OR PERFORMANCE OF THE SOFTWARE REMAINS WITH YOU.
+9. **Limitation of Liability**: TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW,
+   IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
+   INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
+   BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
+   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
+   LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
+   OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE SOFTWARE, EVEN IF ADVISED
+   OF THE POSSIBILITY OF SUCH DAMAGE.
+
+Export and Compliance
+10. You are responsible for complying with applicable export control laws and
+    regulations when distributing the Software.
+
+Contributions
+11. By submitting contributions (including pull requests) to this repository, you
+    grant the copyright holder and other recipients a perpetual, worldwide,
+    non-exclusive, royalty-free license to use, reproduce, modify, and distribute
+    those contributions under the terms of this License.
+
+Termination
+12. This License and the rights granted hereunder will terminate automatically if You
+    fail to comply with any term(s) of this License. Upon termination, You must cease
+    all use and distribution of the Software and destroy all copies in your possession,
+    except as required by law.
+
+Governing Law
+13. This License shall be governed by and construed in accordance with the laws of
+    Bosnia and Herzegovina, without regard to conflict of law principles.
+
+Miscellaneous
+14. If any provision of this License is held to be unenforceable, such provision shall
+    be reformed only to the extent necessary to make it enforceable, and the remaining
+    provisions shall remain in full force and effect.
+
+How to apply this license to your repository
+- This file is the authoritative LICENSE for the repository.
+- Suggested short header for source files:
+  // SPDX-License-Identifier: KSVL-1.0
+
*** End Patch


## 📧 Support

For issues and questions:
- GitHub Issues: [Report an issue](https://github.com/OPKOP-TRIVIUM-sha365/kms-signature-verifier/issues)
- Security: See SECURITY.md for responsible disclosure

---

**Made by:** Vildan KULJANOVIĆ (OPKOP-TRIVIUM-sha365)  
**Last Updated:** 2026-07-04  
**Status:** Production Ready ✅
