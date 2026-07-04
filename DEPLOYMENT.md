# Deployment Guide

Professional deployment instructions for KMS Signature Verifier in production environments.

## 📋 Pre-Deployment Checklist

- [ ] Python 3.11+ installed
- [ ] All dependencies in `requirements.txt` reviewed
- [ ] GPG 2.2+ installed and configured
- [ ] Audit log files prepared
- [ ] Public keys validated independently
- [ ] GitHub Actions secrets configured
- [ ] Network isolation verified (for offline verification)
- [ ] Access control policies defined

## 🚀 Local Deployment

### 1. Install Dependencies

```bash
# Clone repository
git clone https://github.com/OPKOP-TRIVIUM-sha365/kms-signature-verifier.git
cd kms-signature-verifier

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python3 verify_kms_signature.py --help
python3 convert_public_key.py --help
python3 sign_and_verify_msg.py --help
```

### 3. Run Tests

```bash
pytest tests/ -v --cov=.
```

## 🐳 Docker Deployment

### Build Image

```bash
docker build -f docker/Dockerfile -t kms-verifier:1.0 .
docker tag kms-verifier:1.0 kms-verifier:latest
```

### Run Container

```bash
# Interactive mode
docker run -it --rm \
  -v $(pwd)/audit_logs:/audit_logs \
  -v $(pwd)/reports:/reports \
  kms-verifier:latest bash

# Run verification
docker run --rm \
  -v $(pwd)/audit_logs:/audit_logs \
  -v $(pwd)/reports:/reports \
  kms-verifier:latest \
  python3 verify_kms_signature.py \
  --file /audit_logs/audit.json \
  --sig /audit_logs/audit.json.sig \
  --pub /audit_logs/kms_public.der
```

### Push to Registry

```bash
# Docker Hub
docker tag kms-verifier:1.0 username/kms-verifier:1.0
docker push username/kms-verifier:1.0

# GitHub Container Registry
docker tag kms-verifier:1.0 ghcr.io/OPKOP-TRIVIUM-sha365/kms-verifier:1.0
docker push ghcr.io/OPKOP-TRIVIUM-sha365/kms-verifier:1.0
```

## 🔒 GitHub Actions Deployment

### 1. Configure Secrets

Add to GitHub Repository Settings → Secrets and Variables:

```
GPG_PASSPHRASE        # GPG key passphrase (if needed)
AUDIT_LOG_PATH        # Path to audit log
PUBLIC_KEY_PATH       # Path to public key
```

### 2. Enable Workflow

```bash
# List workflows
gh workflow list

# Enable workflow
gh workflow enable verify-and-upload.yml

# Trigger workflow
gh workflow run verify-and-upload.yml
```

### 3. Manual Trigger

```bash
gh workflow run verify-and-upload.yml \
  -f audit_log_path=audit_log.json \
  -f public_key_path=kms_public.der
```

## 🔑 Key Management

### Generate KMS Keys (AWS Example)

```bash
# Create KMS key
aws kms create-key \
  --description "KMS Signature Verification Key" \
  --key-usage SIGN_VERIFY

# Export public key
aws kms get-public-key \
  --key-id <key-id> \
  --query 'PublicKey' \
  --output text | base64 -d > kms_public.der
```

### Convert Keys

```bash
# Base64 to DER/PEM
python3 convert_public_key.py \
  --in public_key_base64.txt \
  --out-der kms_public.der \
  --out-pem kms_public.pem
```

### Verify Key Fingerprint

```bash
# Compute fingerprint
python3 verify_kms_signature.py \
  --file dummy.json \
  --sig dummy.sig \
  --pub kms_public.der | grep fingerprint

# Compare with independent source
# Send fingerprint through secure channel (e.g., phone call)
```

## 📊 Monitoring & Logging

### Check Workflow Runs

```bash
# List recent runs
gh run list --workflow verify-and-upload.yml

# View run details
gh run view <run-id>

# View logs
gh run view <run-id> --log
```

### Artifact Management

```bash
# Download artifacts
gh run download <run-id> -n kms-verification-<run-id>

# List artifacts
ls -la kms-verification-<run-id>/
```

## 🚨 Troubleshooting

### Issue: "Permission denied" on script

```bash
chmod +x verify_kms_signature.py
chmod +x convert_public_key.py
chmod +x sign_and_verify_msg.py
chmod +x sign_and_verify_msg.sh
```

### Issue: "GPG not found"

```bash
# Linux (Debian/Ubuntu)
sudo apt-get install gnupg gnupg2

# macOS
brew install gnupg

# Verify installation
gpg --version
```

### Issue: "Invalid signature"

1. Verify file integrity: `sha256sum audit_log.json`
2. Ensure signature file is binary (not ASCII-armored)
3. Confirm key matches signature
4. Check fingerprint matches independently

### Issue: Python dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install from requirements
pip install -r requirements.txt --force-reinstall

# Verify installation
pip list
```

## 📈 Performance Tuning

| Parameter | Current | Recommendation |
|-----------|---------|-----------------|
| Timeout | 30s | Adjust based on workload |
| Max Message Size | 1MB | Increase for larger files |
| Log Level | INFO | Use DEBUG for troubleshooting |
| Artifact Retention | 90 days | Adjust per compliance |

## 🔄 Backup & Recovery

### Backup Configuration

```bash
# Backup scripts
tar -czf kms-verifier-backup-$(date +%Y%m%d).tar.gz \
  *.py *.sh requirements.txt .github/workflows/

# Backup public keys
tar -czf kms-keys-backup-$(date +%Y%m%d).tar.gz \
  *.der *.pem

# Store in secure location
```

### Recovery Procedures

```bash
# Restore from backup
tar -xzf kms-verifier-backup-20260704.tar.gz

# Reinstall dependencies
pip install -r requirements.txt

# Re-test functionality
pytest tests/ -v
```

## 🎯 Success Criteria

✅ **Deployment successful when:**
- All tests pass (`pytest`)
- Script execution successful (exit code 0)
- JSON reports generate correctly
- GitHub Actions workflow runs without errors
- Artifacts upload successfully

## 📞 Support

For deployment issues:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review workflow logs: `gh run view <run-id> --log`
3. Report issues: GitHub Issues or email

---

**Last Updated:** 2026-07-04  
**Maintained by:** Vildan KULJANOVIĆ
