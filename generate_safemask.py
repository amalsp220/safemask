#!/usr/bin/env python3
"""SafeMask Project Generator - Creates complete package structure."""

import os
from pathlib import Path

def create_file(filepath: str, content: str) -> None:
    """Create file and parent directories."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"✓ {filepath}")

print("Generating SafeMask Project...")
print()

# ===== CORE MODULES =====
create_file("safemask/__init__.py", '''"""SafeMask: Privacy-Preserving Text Processing Engine."""
from .engine import SafeMaskEngine, mask_text
from .types import MaskingStyle, SensitiveCategory

__version__ = "1.0.0"
__author__ = "Amal"
__license__ = "MIT"

__all__ = ["mask_text", "SafeMaskEngine", "SensitiveCategory", "MaskingStyle"]
''')

create_file("safemask/types.py", '''"""Type definitions for SafeMask."""
from enum import Enum
from typing import TypedDict

class MaskingStyle(str, Enum):
    PARTIAL = "partial"
    FULL = "full"
    TOKEN = "token"

class SensitiveCategory(str, Enum):
    AADHAAR = "aadhaar"
    PAN = "pan"
    PASSPORT = "passport"
    VOTER_ID = "voter_id"
    DRIVING_LICENSE = "driving_license"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_ACCOUNT = "bank_account"
    IFSC = "ifsc"
    SWIFT = "swift"
    IBAN = "iban"
    UPI = "upi"
    PHONE = "phone"
    EMAIL = "email"
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    API_KEY = "api_key"
    JWT = "jwt"
    ACCESS_TOKEN = "access_token"
    SESSION_ID = "session_id"
    OTP = "otp"

class DetectionResult(TypedDict):
    category: SensitiveCategory
    start: int
    end: int
    value: str
    valid: bool
''')

print("\nCore modules created successfully!")
print("Run 'pip install -e \".[dev]\"' to install dependencies.")
print("Run 'pytest tests/' to run tests.")
