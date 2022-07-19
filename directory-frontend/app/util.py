"""Shared utility helper functions"""
import os

def random_hex_bytes(n_bytes):
    """Create a hex encoded string of random bytes"""
    return os.urandom(n_bytes).hex()
