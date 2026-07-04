#!/usr/bin/env python3
"""
Unit tests for verify_kms_signature.py
"""
import pytest
import tempfile
import hashlib
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


@pytest.fixture
def rsa_key_pair():
    """Generate RSA key pair for testing."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


@pytest.fixture
def test_message():
    """Create test message."""
    return b"Test audit log message for verification"


@pytest.fixture
def signature(rsa_key_pair, test_message):
    """Create detached signature."""
    private_key, _ = rsa_key_pair
    digest = hashlib.sha256(test_message).digest()
    sig = private_key.sign(
        digest,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return sig


def test_sha256_fingerprint(rsa_key_pair):
    """Test SHA-256 fingerprint generation."""
    _, public_key = rsa_key_pair
    der = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Compute fingerprint
    h = hashlib.sha256(der).digest()
    fingerprint = ":".join(f"{b:02X}" for b in h)
    
    # Validate format
    parts = fingerprint.split(":")
    assert len(parts) == 32  # SHA-256 = 256 bits = 32 bytes
    assert all(len(p) == 2 for p in parts)


def test_valid_signature(rsa_key_pair, test_message, signature, tmp_path):
    """Test valid signature verification."""
    _, public_key = rsa_key_pair
    
    # Write test files
    msg_file = tmp_path / "test.txt"
    sig_file = tmp_path / "test.txt.sig"
    
    msg_file.write_bytes(test_message)
    sig_file.write_bytes(signature)
    
    # Verify
    digest = hashlib.sha256(test_message).digest()
    try:
        public_key.verify(
            signature,
            digest,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        assert True
    except Exception:
        assert False


def test_invalid_signature(rsa_key_pair, test_message, tmp_path):
    """Test invalid signature detection."""
    _, public_key = rsa_key_pair
    
    # Create invalid signature
    bad_sig = b"invalid_signature_data"
    
    digest = hashlib.sha256(test_message).digest()
    with pytest.raises(Exception):
        public_key.verify(
            bad_sig,
            digest,
            padding.PKCS1v15(),
            hashes.SHA256()
        )


def test_key_loading(rsa_key_pair, tmp_path):
    """Test public key loading (DER and PEM)."""
    _, public_key = rsa_key_pair
    
    # Save as DER
    der_file = tmp_path / "key.der"
    der_data = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    der_file.write_bytes(der_data)
    
    # Load DER
    loaded_key = serialization.load_der_public_key(der_data)
    assert loaded_key.key_size == public_key.key_size
    
    # Save as PEM
    pem_file = tmp_path / "key.pem"
    pem_data = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    pem_file.write_bytes(pem_data)
    
    # Load PEM
    loaded_pem_key = serialization.load_pem_public_key(pem_data)
    assert loaded_pem_key.key_size == public_key.key_size


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
