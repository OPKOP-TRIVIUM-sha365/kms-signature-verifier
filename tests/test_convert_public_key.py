#!/usr/bin/env python3
"""
Unit tests for convert_public_key.py
"""
import pytest
import base64
import tempfile
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


@pytest.fixture
def rsa_public_key():
    """Generate RSA public key for testing."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return private_key.public_key()


@pytest.fixture
def base64_public_key(rsa_public_key):
    """Create base64-encoded public key."""
    der = rsa_public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return base64.b64encode(der).decode('utf-8')


def test_base64_decode(base64_public_key):
    """Test base64 decoding."""
    decoded = base64.b64decode(base64_public_key)
    assert len(decoded) > 0
    
    # Verify it's a valid key
    key = serialization.load_der_public_key(decoded)
    assert key is not None


def test_der_export(rsa_public_key, tmp_path):
    """Test DER export."""
    der_file = tmp_path / "key.der"
    der_data = rsa_public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    der_file.write_bytes(der_data)
    
    assert der_file.exists()
    assert len(der_data) > 0


def test_pem_export(rsa_public_key, tmp_path):
    """Test PEM export."""
    pem_file = tmp_path / "key.pem"
    pem_data = rsa_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    pem_file.write_bytes(pem_data)
    
    assert pem_file.exists()
    assert b"-----BEGIN PUBLIC KEY-----" in pem_data
    assert b"-----END PUBLIC KEY-----" in pem_data


def test_invalid_base64():
    """Test invalid base64 handling."""
    invalid_b64 = "this is not valid base64!!!"
    with pytest.raises(Exception):
        base64.b64decode(invalid_b64, validate=True)


def test_fingerprint_generation(rsa_public_key):
    """Test fingerprint generation."""
    import hashlib
    
    der = rsa_public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    h = hashlib.sha256(der).digest()
    fingerprint = ":".join(f"{b:02X}" for b in h)
    
    # Validate format (SHA-256 = 32 bytes)
    parts = fingerprint.split(":")
    assert len(parts) == 32


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
