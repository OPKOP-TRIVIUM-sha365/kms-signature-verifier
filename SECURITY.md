# Security Policy

## Reporting Security Vulnerabilities

**PLEASE DO NOT** open public issues for security vulnerabilities. Instead, email security details to the maintainers.

### Responsible Disclosure

We take security seriously. If you discover a vulnerability:

1. **Do NOT** create a public GitHub issue
2. **DO** email security details directly
3. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if applicable)

### Response Timeline

- **Initial Response**: Within 24 hours
- **Security Advisory**: Published after fix is released
- **Credit**: Your name will be credited (unless you prefer anonymity)

---

## Security Features

### ✅ Built-in Protections

| Feature | Description |
|---------|-------------|
| **Input Validation** | All inputs validated before processing |
| **Timeout Protection** | 30-second timeout on external commands |
| **Error Handling** | No sensitive data in error messages |
| **Logging** | Comprehensive audit logging |
| **Key Validation** | Public keys validated on load |
| **File Permissions** | Output directory created with 700 permissions |

### ✅ Best Practices

1. **Offline Verification**: Run verification on isolated machines
2. **Fingerprint Verification**: Compare fingerprints via independent channels
3. **Access Control**: Use GitHub RBAC for workflow permissions
4. **Audit Logging**: Enable GitHub Actions audit logging
5. **Key Rotation**: Rotate KMS keys regularly
6. **Secret Management**: Use GitHub Secrets for sensitive data

---

## Known Issues

Currently, no known security issues. Please report any findings.

---

## Dependencies

### Python Packages

| Package | Version | Purpose |
|---------|---------|---------|
| cryptography | >=41.0.0 | Cryptographic operations |
| python-gnupg | >=2.5.0 | GPG integration |

Both dependencies are actively maintained and regularly updated for security patches.

### External Tools

- **GPG/GPG2** (2.2+): Message signing and verification
- **OpenSSL** (optional): Key inspection

---

## Security Audit Checklist

- [x] Input validation for all user inputs
- [x] Timeout protection for external commands
- [x] Proper error handling (no info disclosure)
- [x] Comprehensive logging
- [x] Key format validation
- [x] Detached signature support
- [x] SHA-256 fingerprinting
- [x] GitHub Actions RBAC
- [x] Artifact retention policies
- [x] No hardcoded secrets

---

## Compliance

- **OWASP Top 10**: Addressed key vulnerabilities
- **CWE**: Follows CWE best practices
- **NIST**: Aligned with NIST cryptographic standards

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-07-04 | Initial release |

---

For security inquiries, contact: security@opkop-trivium.example
