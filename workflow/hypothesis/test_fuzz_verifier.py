#!/usr/bin/env python3
"""
OPKOP TRIVIUM :: Automated Fuzz & Edge-Case Testing Suite
Target: Attestation Input Parsing Validation
"""

import pytest
from hypothesis import given, strategies as st
from attestation_engine import EnclaveAttestationEngine

# Inicijalizacija motora s fiksnim očekivanim PCR-om za testiranje
test_pcrs = {"0": "9b8fbba34f130995865939eae1b34741cafe70e669498b16ad45dd294383bc6f"}
engine = EnclaveAttestationEngine(expected_pcrs=test_pcrs)

def test_deterministic_edge_cases():
    """Ručno testiranje ekstremno malformiranih i praznih struktura podataka."""
    print("[TEST] Izvršavanje determinističkih edge-case testova...")
    
    # Slučaj A: Prazan rječnik (No Crash Rule)
    assert engine.verify_hardware_quote({}) is False
    
    # Slučaj B: Korumpirani PCR ključevi
    corrupted_quote = {"enclave_metadata": "MOCK", "pcrs": {"0": "BAD_HASH_VIL_1108"}}
    assert engine.verify_hardware_quote(corrupted_quote) is False
    
    # Slučaj C: Nedostaje sekcija metapodataka
    incomplete_quote = {"pcrs": {"0": "9b8fbba34f130995865939eae1b34741cafe70e669498b16ad45dd294383bc6f"}}
    assert engine.verify_hardware_quote(incomplete_quote) is False

@given(st.dictionaries(
    keys=st.text(min_size=1, max_size=10),
    values=st.text(min_size=1, max_size=100)
))
def test_fuzz_random_json_injection(fuzzed_dict):
    """
    PRIORITET 4: Fuzz testing pomoću Hypothesis-a.
    Generira nasumične strukture i ubacuje ih u parser kako bi provjerio stabilnost.
    """
    # Sustav smije vratiti False (odbijanje), ali nikada ne smije baciti neočekivani Exception (Unhandled Crash)
    result = engine.verify_hardware_quote(fuzzed_dict)
    assert result is False

if __name__ == "__main__":
    print("[+] Pokretanje robusnog testnog okvira...")
    test_deterministic_edge_cases()
    print("[+] Svi deterministički edge-case testovi PROŠLI.")
