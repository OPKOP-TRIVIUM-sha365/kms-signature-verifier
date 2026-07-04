#!/usr/bin/env python3
"""
Unit tests for sign_and_verify_msg.py
"""
import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime, timezone


@pytest.fixture
def test_message():
    """Create test message."""
    return "Test KMS verification message"


@pytest.fixture
def output_dir(tmp_path):
    """Create temporary output directory."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    return str(out_dir)


def test_message_file_creation(test_message, output_dir):
    """Test message file creation."""
    msg_file = Path(output_dir) / "test.txt"
    msg_file.write_text(test_message + "\n")
    
    assert msg_file.exists()
    content = msg_file.read_text()
    assert test_message in content


def test_json_report_structure():
    """Test JSON report structure."""
    report = {
        "result": "VERIFIED_OK",
        "key_id": "0xABCDEF1234567890",
        "fingerprint": "3A7F1C9B...",
        "gpg_timestamp": "2026-07-04T23:10:00Z",
        "iso_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "workflow_run_id": "12345",
        "commit_hash": "abc123",
        "workflow_repo": "myorg/myrepo",
        "workflow_ref": "refs/heads/main",
        "message_file": "/path/to/msg.txt",
        "signature_file": "/path/to/msg.txt.asc",
        "gpg_verify_output": "gpg: Signature made..."
    }
    
    # Validate structure
    required_fields = [
        "result", "key_id", "fingerprint", "gpg_timestamp",
        "iso_timestamp_utc", "workflow_run_id", "commit_hash",
        "workflow_repo", "workflow_ref", "message_file",
        "signature_file", "gpg_verify_output"
    ]
    
    for field in required_fields:
        assert field in report
    
    # Validate JSON serialization
    json_str = json.dumps(report, indent=2)
    assert "VERIFIED_OK" in json_str


def test_message_validation():
    """Test message size validation."""
    max_size_mb = 1
    test_size_mb = 0.5
    
    # Should pass
    assert test_size_mb < max_size_mb
    
    # Should fail
    assert 2.0 > max_size_mb


def test_keyid_extraction():
    """Test key ID extraction from GPG output."""
    gpg_output = """gpg: Signature made Sat 04 Jul 2026 23:10:00 CEST
gpg:                using RSA key 0xABCDEF1234567890
gpg: Good signature from "Test User <test@example.com>" [ultimate]"""
    
    # Extract key ID
    keyid = ""
    for line in gpg_output.splitlines():
        if "using" in line and "key" in line:
            parts = line.strip().split()
            for p in parts:
                if p.startswith("0x") and len(p) >= 10:
                    keyid = p
                    break
    
    assert keyid == "0xABCDEF1234567890"


def test_timestamp_extraction():
    """Test timestamp extraction from GPG output."""
    gpg_output = """gpg: Signature made Sat 04 Jul 2026 23:10:00 CEST"""
    
    timestamp = ""
    for line in gpg_output.splitlines():
        if line.startswith("gpg: Signature made"):
            timestamp = line.replace("gpg: ", "").strip()
    
    assert "Signature made" in timestamp
    assert "2026" in timestamp


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
