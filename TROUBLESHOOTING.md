# Troubleshooting Guide

Common issues and solutions for KMS Signature Verifier.

## 🔍 Diagnostic Steps

Before troubleshooting, gather information:

```bash
# Check Python version
python3 --version

# Check GPG installation
gpg --version

# Check dependencies
pip list | grep -E "cryptography|gnupg"

# Enable verbose logging
export LOGLEVEL=DEBUG
python3 verify_kms_signature.py --file audit.json --sig audit.json.sig --pub kms_public.der --verbose
```

## ❌ Common Issues

### Issue 1: "GPG not found"

**Symptoms:**
```
ERROR: GPG not found in system
```

**Solutions:**

```bash
# Debian/Ubuntu
sudo apt-get update
sudo apt-get install gnupg gnupg2

# macOS
brew install gnupg

# CentOS/RHEL
sudo yum install gnupg

# Verify installation
which gpg2
gpg2 --version
```

**Alternative:** Set GPG path manually
```bash
export PATH="/usr/bin/gpg2:$PATH"
python3 sign_and_verify_msg.py --file msg.txt
```

---

### Issue 2: "Permission denied"

**Symptoms:**
```
Permission denied: ./verify_kms_signature.py
```

**Solutions:**

```bash
# Make scripts executable
chmod +x verify_kms_signature.py
chmod +x convert_public_key.py
chmod +x sign_and_verify_msg.py
chmod +x sign_and_verify_msg.sh

# Verify permissions
ls -la *.py *.sh
```

---

### Issue 3: "Failed to load public key"

**Symptoms:**
```
ERROR: cannot load public key: Failed to load public key (DER/PEM)
```

**Solutions:**

```bash
# Check file format
file kms_public.der
file kms_public.pem

# Inspect DER key
openssl pkey -pubin -inform DER -in kms_public.der -text -noout

# Inspect PEM key
openssl pkey -pubin -in kms_public.pem -text -noout

# Validate with Python
python3 << 'EOF'
from cryptography.hazmat.primitives import serialization
with open('kms_public.der', 'rb') as f:
    key = serialization.load_der_public_key(f.read())
    print(f"Key type: {key.__class__.__name__}")
    print(f"Key size: {key.key_size}")
EOF
```

---

### Issue 4: "INVALID SIGNATURE"

**Symptoms:**
```
INVALID SIGNATURE
exit code: 2
```

**Solutions:**

1. **Verify file integrity:**
```bash
sha256sum audit_log.json
# Compare with known hash
```

2. **Check signature file format:**
```bash
# Should be binary, not text
file audit_log.json.sig
hexdump -C audit_log.json.sig | head

# If ASCII-armored, extract binary:
gpg2 --output audit_log.json.sig.bin audit_log.json.sig
```

3. **Verify with GPG directly:**
```bash
gpg2 --verify audit_log.json.sig audit_log.json
```

4. **Confirm key matches:**
```bash
# List available keys
gpg2 --list-keys

# Export public key
gpg2 --export --armor <keyid> > key.asc

# Compare fingerprints
gpg2 --fingerprint <keyid>
python3 verify_kms_signature.py --file audit.json --sig audit.json.sig --pub key.asc
```

---

### Issue 5: "Input is not valid base64"

**Symptoms:**
```
ERROR: Input is not valid base64
```

**Solutions:**

```bash
# Check file content
head -c 100 public_key_base64.txt

# Validate base64
python3 << 'EOF'
import base64
with open('public_key_base64.txt', 'r') as f:
    content = f.read().strip()
    try:
        decoded = base64.b64decode(content, validate=True)
        print(f"Valid base64: {len(decoded)} bytes")
    except Exception as e:
        print(f"Invalid: {e}")
EOF

# Remove whitespace/newlines
tr -d '\n' < public_key_base64.txt > public_key_base64_clean.txt
```

---

### Issue 6: "Message file too large"

**Symptoms:**
```
ERROR: Message file too large: 2.50MB (max 1MB)
```

**Solutions:**

```bash
# Check file size
du -h msg.txt

# Compress
gzip msg.txt

# Or modify script (max_size_mb parameter)
python3 sign_and_verify_msg.py --file large_msg.txt --out out
# Edit script to increase max_size_mb in validate_message()
```

---

### Issue 7: "Python dependencies missing"

**Symptoms:**
```
ModuleNotFoundError: No module named 'cryptography'
```

**Solutions:**

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install cryptography>=41.0.0
pip install python-gnupg>=2.5.0

# Verify installation
python3 -c "import cryptography; print(cryptography.__version__)"
python3 -c "import gnupg; print(gnupg.__version__)"
```

---

### Issue 8: "GitHub Actions workflow fails"

**Symptoms:**
```
Error: Audit log not found: audit_log.json
```

**Solutions:**

1. **Verify file paths:**
```bash
# Ensure files exist in repo root
git ls-files | grep -E "audit|\.der|\.pem"
```

2. **Check workflow permissions:**
```yaml
permissions:
  contents: read
  actions: read
  checks: write
```

3. **Enable workflow:**
```bash
gh workflow enable verify-and-upload.yml
gh workflow list
```

4. **View logs:**
```bash
gh run view <run-id> --log
```

---

### Issue 9: "Timeout during verification"

**Symptoms:**
```
ERROR: GPG command timed out (30s)
```

**Solutions:**

```bash
# Run with increased timeout (edit script)
# Change: timeout=30 to timeout=60

# Or use GPG directly
gpg2 --verify audit_log.json.sig audit_log.json

# Check GPG daemon status
gpg-connect-agent /bye
```

---

### Issue 10: "Artifact upload fails"

**Symptoms:**
```
Error: Failed to upload artifact
```

**Solutions:**

```bash
# Check output directory permissions
ls -la out/

# Fix permissions
chmod 755 out/
chmod 644 out/*

# Verify artifact content
ls -la out/verify_report.json
cat out/verify_report.json | python3 -m json.tool
```

---

## 🧪 Testing & Validation

### Run Quick Tests

```bash
# Unit tests
pytest tests/ -v

# Coverage report
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html
```

### Manual Verification

```bash
# 1. Generate test data
python3 << 'EOF'
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from pathlib import Path
import hashlib

# Generate key pair
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Save public key
pub_der = public_key.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
Path("test_pub.der").write_bytes(pub_der)

# Create test message
test_msg = b"Test audit log"
Path("test_msg.json").write_bytes(test_msg)

# Sign
digest = hashlib.sha256(test_msg).digest()
sig = private_key.sign(digest, padding.PKCS1v15(), hashes.SHA256())
Path("test_msg.json.sig").write_bytes(sig)

print("✓ Test files created")
EOF

# 2. Verify signature
python3 verify_kms_signature.py \
  --file test_msg.json \
  --sig test_msg.json.sig \
  --pub test_pub.der \
  --verbose
```

---

## 📊 Performance Debugging

### Profile Execution

```bash
python3 -m cProfile -s cumtime verify_kms_signature.py \
  --file audit.json \
  --sig audit.json.sig \
  --pub kms_public.der
```

### Memory Usage

```bash
pip install memory_profiler
python3 -m memory_profiler verify_kms_signature.py \
  --file audit.json \
  --sig audit.json.sig \
  --pub kms_public.der
```

---

## 🆘 Getting Help

### Debug Information

Gather before reporting issues:

```bash
#!/bin/bash
echo "=== System Info ==="
uname -a
python3 --version
gpg --version

echo "=== Python Packages ==="
pip list

echo "=== File Information ==="
ls -lah audit_log.json*
file audit_log.json.sig
file kms_public.der

echo "=== GPG Keys ==="
gpg2 --list-keys

echo "=== Recent Logs ==="
tail -50 /var/log/syslog 2>/dev/null || tail -50 /var/log/system.log 2>/dev/null
```

### Report Issue

Create GitHub issue with:
1. Error message (full output)
2. Debug information (script output above)
3. Steps to reproduce
4. Expected vs actual behavior

---

**Last Updated:** 2026-07-04  
**Version:** 1.0
