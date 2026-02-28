"""SafeMask: Privacy-Preserving Text Processing Engine.

Detect, validate, and intelligently mask sensitive information in text.
"""

from typing import List, Optional, Iterable
import re
from enum import Enum

__version__ = "1.0.0"
__author__ = "Amal"
__license__ = "MIT"

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

class SafeMaskEngine:
    """Privacy-Preserving Text Processing Engine."""
    
    PATTERNS = {
        SensitiveCategory.EMAIL: r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        SensitiveCategory.PHONE: r'\+?[0-9]{1,3}[-.]?[0-9]{1,14}',
        SensitiveCategory.CREDIT_CARD: r'\b(?:\d[\s-]*?){13,19}\b',
        SensitiveCategory.IPV4: r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
        SensitiveCategory.AADHAAR: r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
        SensitiveCategory.PAN: r'[A-Z]{5}[0-9]{4}[A-Z]{1}',
    }
    
    def __init__(self, token_replacement: str = "[MASKED]", partial_visible_chars: int = 4):
        self.token_replacement = token_replacement
        self.partial_visible_chars = partial_visible_chars
    
    def detect(self, text: str, categories: Optional[Iterable[str]] = None) -> List[dict]:
        """Detect sensitive data in text."""
        results = []
        categories_to_check = categories if categories else [c.value for c in SensitiveCategory]
        
        for category_value in categories_to_check:
            try:
                category = SensitiveCategory(category_value)
            except ValueError:
                continue
            
            pattern = self.PATTERNS.get(category)
            if pattern:
                for match in re.finditer(pattern, text):
                    results.append({
                        'category': category_value,
                        'start': match.start(),
                        'end': match.end(),
                        'value': match.group(),
                        'valid': True
                    })
        
        return sorted(results, key=lambda x: x['start'])
    
    def mask(self, value: str, style: MaskingStyle = MaskingStyle.PARTIAL) -> str:
        """Mask a value based on style."""
        if style == MaskingStyle.FULL or style == MaskingStyle.TOKEN:
            return self.token_replacement
        if style == MaskingStyle.PARTIAL:
            if len(value) <= self.partial_visible_chars:
                return self.token_replacement
            visible = value[:self.partial_visible_chars]
            return visible + "*" * (len(value) - self.partial_visible_chars)
        return value
    
    def mask_text(self, text: str, categories: Optional[Iterable[str]] = None, style: MaskingStyle = MaskingStyle.PARTIAL) -> str:
        """Mask sensitive data in text."""
        detections = self.detect(text, categories)
        if not detections:
            return text
        
        chars = list(text)
        for detection in sorted(detections, key=lambda x: x['start'], reverse=True):
            masked = self.mask(detection['value'], style)
            start, end = detection['start'], detection['end']
            chars[start:end] = list(masked)
        
        return ''.join(chars)

def mask_text(text: str, categories: Optional[Iterable[str]] = None, style: MaskingStyle = MaskingStyle.PARTIAL) -> str:
    """Mask sensitive data in text."""
    engine = SafeMaskEngine()
    return engine.mask_text(text, categories, style)

__all__ = ["mask_text", "SafeMaskEngine", "SensitiveCategory", "MaskingStyle"]
